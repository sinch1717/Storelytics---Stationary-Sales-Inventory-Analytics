"""
Om Stationeries — Sales & Inventory Processor
==============================================
WHAT THIS SCRIPT DOES:
  Script 1 — Cleans Sales_Data_Entry.csv → produces Sales_Data.csv
    • Standardises dates (DD.MM.YY → DD-MM-YYYY)
    • Splits Name/company into Brand + Product Name
    • Looks up SKU from Inventory_Data.csv
    • Flags rows needing review

  Script 2 — Updates Inventory_Data.csv
    • For every sale with no matching SKU, adds a new skeleton row
    • Rate, Qty, Cost Price left blank for you to fill
    • Category/Sub-category set to UNKNOWN for you to fill

HOW TO USE:
  1. Export from Google Sheets as CSV:
       - Sales_Data_Entry  → Sales_Data_Entry.csv
       - Inventory_Data    → Inventory_Data.csv
  2. Place both CSVs in the same folder as this script
  3. Run:  python3 om_stationeries.py
  4. Import outputs back into Google Sheets:
       - Sales_Data.csv        → Sales_Data sheet
       - Inventory_Data.csv    → Inventory_Data sheet (updated)

TO ADD NEW SALES DATA:
  Just add new rows to your Sales_Data_Entry sheet in Google Sheets,
  re-export as CSV, and run the script again.
  It will only process rows not already in Sales_Data.csv.

INPUT FILES:
  Sales_Data_Entry.csv    — raw sales entry (exported from Google Sheets)
  Inventory_Data.csv      — inventory master with SKUs

OUTPUT FILES:
  Sales_Data.csv          — cleaned, SKU-mapped sales (import as new sheet)
  Inventory_Data.csv      — updated with any new skeleton rows
"""

import pandas as pd
import re
import os
import sys
from datetime import datetime

# FILE NAMES 
SALES_ENTRY_FILE = "D:\\IITMDS\\Diploma in programmin\\BDM project\\stationary\\python scripts\\to be uploaded\\BDM Data - Sales_Data_Entry.csv"
INVENTORY_FILE   = "D:\\IITMDS\\Diploma in programmin\\BDM project\\stationary\\python scripts\\to be uploaded\\BDM Data - Inventory_Data.csv"
SALES_OUTPUT_FILE = "Sales_Data.csv"

 
# KNOWN BRANDS
# Add any new brands here as stock grows
 
KNOWN_BRANDS = [
    # Pens & writing
    "Doms", "Camlin", "Classmate", "Faber Castell", "Faber-Castell",
    "Apsara", "Nataraja", "Nataraj", "Youva", "Kores", "Reynolds",
    "Pilot", "Parker", "Addgel", "Hauser", "Linograph", "Robercastle",
    "Papersoft", "PaperSoft", "Butterflow", "XO", "Uni", "Artline",
    "Maped", "Staedtler", "Pentel", "Octane", "Montex", "Maxter",
    "Unomax", "Flair", "Pentonic", "Uniball", "Energel", "Curve",
    "Kones", "Boms", "Orbit", "Amigo", "Casio", "Kangaroo", "Ritco",
    "Sandisk", "Canon", "Epson", "Boat", "Vicky", "Duracell",
    "Scotch", "Uni Posca", "Camel", "Fevicol", "Fevistick",
    "Fevibond", "Fevikwik", "Fevicril", "HP", "Khyathi", "Hot Wheels",
    "Hotwheels", "PB Birds",
]

# Sort longest first so "Faber Castell" matches before "Faber"
KNOWN_BRANDS = sorted(set(KNOWN_BRANDS), key=len, reverse=True)

 
# CATEGORY & SUBCATEGORY CODES (for new SKU generation)
 
CATEGORY_CODES = {
    "Writing Instruments":            "WI",
    "Paper Products":                 "PP",
    "Files and Folders":              "FF",
    "Office Desk Supplies":           "OD",
    "Adhesives & Tapes":              "AT",
    "Correction & Erasing Items":     "CE",
    "Measurement & Geometry Tools":   "MG",
    "Art & Craft Supplies":           "AC",
    "School-Specific Supplies":       "SS",
    "Office Forms & Registers":       "OF",
    "Printing & Computer Stationery": "PC",
    "Fasteners & Binding Materials":  "FB",
    "Envelopes & Mailing Supplies":   "EM",
    "Miscellaneous / Utility Items":  "MU",
    "Toys & Games":                   "TG",
    "Electronics & Accessories":      "EL",
    "Services":                       "SV",
    "UNKNOWN":                        "XX",
}

SUBCATEGORY_CODES = {
    "Pens": "PEN", "Pencils": "PCL", "Markers": "MRK",
    "Highlighters": "HLT", "Sketching & Colour Writing": "SKC",
    "Chalk & Board Writing": "CBW", "Sharpening & Pencil Maintenance": "SHP",
    "Accessories for Writing Instruments": "AWI",
    "Notebooks & Writing Books": "NWB", "Registers & Office Books": "ROB",
    "Loose Writing Paper": "LWP", "Printing & Copier Paper": "PCP",
    "Drawing & Art Paper": "DAP", "Craft & Decorative Paper": "CDP",
    "Card & Board Paper": "CBP", "Technical & Specialty Paper": "TSP",
    "Sticky & Label Paper": "SLP", "Envelopes & Mailing Paper": "EMP",
    "Diaries & Planners": "DPL", "Academic & Exam Paper": "AEP",
    "Packaging & Wrapping Paper": "PWP", "Rolls & Large Format Paper": "RLF",
    "Basic Files": "BFL", "Plastic Files": "PLF",
    "Display & Presentation Files": "DPF", "Ring Binder Files": "RBF",
    "Lever Arch & Office Files": "LAF", "Expanding Files": "EXF",
    "Box & Storage Files": "BSF", "Academic / Project Files": "APF",
    "Legal & Government Files": "LGF", "File Accessories": "FAC",
    "Stapling Supplies": "STS", "Pinning Supplies": "PIN",
    "Punching Tools": "PUN", "Cutting Tools": "CUT",
    "Clipping & Fastening": "CLF", "Adhesive Handling": "ADH",
    "Measuring Tools": "MST", "Desk Organization": "DSO",
    "Display & Desk Items": "DDI", "Miscellaneous Desk Items": "MDI",
    "Liquid Adhesives": "LQA", "Glue Sticks": "GLS",
    "Instant Adhesives": "INS", "Industrial / Strong Adhesives": "ISA",
    "Tape Types": "TAP", "Specialty Tapes": "SPT",
    "Glue Application Tools": "GAT", "Adhesive Accessories": "AAC",
    "Erasers": "ERS", "Correction Fluids": "CFL", "Correction Pens": "CPE",
    "Correction Tapes": "CTP", "Erasing Devices": "ERD",
    "Rulers & Scales": "RLS", "Compasses": "CMP", "Dividers": "DIV",
    "Protractors": "PRO", "Set Squares": "SSQ", "Geometry Sets / Boxes": "GEO",
    "Measuring Instruments": "MIN", "Drafting Tools": "DFT",
    "Accessories": "ACC",
    "Colouring Supplies": "COL", "Paints": "PNT", "Brushes": "BRS",
    "Drawing Materials": "DRM", "Craft Papers & Sheets": "CPS",
    "Craft Decoration Materials": "CDM", "Clay & Modelling": "CLY",
    "Cutting & Craft Tools": "CCT", "Adhesives for Craft": "AFC",
    "Painting Surfaces": "PAS", "DIY & Craft Kits": "DIY",
    "Board & Sheet Materials": "BSM", "Specialty Craft Materials": "SCM",
    "Writing & Study Essentials": "WSE", "School Bags & Carry Items": "SBC",
    "Identification & Labels": "IDL", "Book Protection": "BKP",
    "Learning Tools": "LTL", "Exam & Academic Supplies": "EAS",
    "Diaries & School Records": "DSR", "Student Accessories": "STA",
    "Accounting Registers": "ACR", "Attendance & Staff Records": "ASR",
    "Inventory & Stock Records": "ISR", "Billing & Transaction Books": "BTB",
    "Receipt & Payment Records": "RPR", "Order & Dispatch Records": "ODR",
    "Administrative Records": "ADR", "Pre-Printed Office Forms": "PPF",
    "Miscellaneous Office Books": "MOB",
    "Copier & Printer Paper": "CPP", "Photo & Specialty Printing Paper": "PSP",
    "Label & Sticker Sheets": "LSS", "Continuous & Dot Matrix Paper": "CDT",
    "Billing & Thermal Paper": "BTP", "Printer Consumables": "PRC",
    "Data Storage Media": "DSM", "Computer Forms & Sheets": "CFS",
    "Paper Fasteners": "PAF", "Pin & Tag Fasteners": "PTF",
    "Metal Fasteners": "MTF", "Elastic Fasteners": "ELF",
    "Binder Rings": "BNR", "Spiral Binding Materials": "SBM",
    "Comb Binding Materials": "CBM",
    "Calculators": "CAL", "Boards & Display Items": "BDI",
    "Board Accessories": "BAC", "Desk Display Items": "DDT",
    "Sealing & Stamping Items": "SSI", "Identification & Tags": "IDT",
    "Miscellaneous Office Tools": "MOT",
    "Die-Cast & Model Vehicles": "DMV", "Puzzle & Strategy Games": "PSG",
    "Action & Soft Toys": "AST", "Sports Toys": "SPO",
    "Storage Devices": "SDE", "Cables & Connectors": "CAB",
    "Audio": "AUD", "Input Devices": "INP", "Batteries": "BAT",
    "Laser & Light Accessories": "LLA",
    "Printer Consumables (Electronics)": "PCE",
    "Reprographics": "RPG", "Printing": "PRT", "Courier": "COU",
    "UNKNOWN": "UNK",
}


# ═════════════════════════════════════════════════════════════════
# HELPERS
# ═════════════════════════════════════════════════════════════════

def standardise_date(val):
    """DD.MM.YY or DD.MM.YYYY → DD-MM-YYYY. Leaves anything else as-is."""
    val = str(val).strip()
    match = re.match(r'^(\d{1,2})\.(\d{1,2})\.(\d{2,4})$', val)
    if match:
        d, m, y = match.groups()
        if len(y) == 2:
            y = "20" + y
        return f"{d.zfill(2)}-{m.zfill(2)}-{y}"
    return val  # already clean or unrecognised format


def split_brand_product(name_str):
    """
    Split 'Brand ProductDescription' into (brand, product_name, needs_review).
    needs_review = True when no known brand found.
    """
    name_str = str(name_str).strip()

    # Try matching brand at START of string
    for brand in KNOWN_BRANDS:
        pattern = re.compile(r'^' + re.escape(brand) + r'[\s,\-]*(.*)', re.IGNORECASE)
        m = pattern.match(name_str)
        if m:
            product = m.group(1).strip()
            # If nothing left after brand, product name = full string (e.g. "Parker")
            if not product:
                product = name_str
            return brand, product, False

    # Try matching brand at END of string (e.g. "Brush size Camlin")
    for brand in KNOWN_BRANDS:
        pattern = re.compile(r'^(.*?)\s+' + re.escape(brand) + r'$', re.IGNORECASE)
        m = pattern.match(name_str)
        if m:
            product = m.group(1).strip()
            return brand, product, False

    # No known brand found — return full string as product, flag for review
    return "", name_str, True


def clean_inv_name(brand, product_name, raw_name):
    """Build clean inventory name, avoiding 'Brand Brand' doubling."""
    if not brand:
        return product_name or raw_name
    # If product_name is empty or is the same as brand (e.g. entry was just "Fevicol")
    if not product_name or product_name.strip().lower() == brand.strip().lower():
        return raw_name
    return f"{brand} {product_name}"


def build_sku_lookup(inv_df):
    """
    Returns dict: lowercase name/alias → SKU Code.
    Checks: Name column + Aliases column (comma-separated).
    """
    lookup = {}
    for _, row in inv_df.iterrows():
        sku = str(row['SKU Code']).strip()
        # Primary name
        lookup[str(row['Name']).strip().lower()] = sku
        # Aliases
        if 'Aliases' in row and pd.notna(row['Aliases']) and str(row['Aliases']).strip():
            for alias in str(row['Aliases']).split(','):
                alias = alias.strip().lower()
                if alias:
                    lookup[alias] = sku
    return lookup


def find_sku(product_name, brand, raw_name, sku_lookup):
    """
    Try to find a matching SKU. Returns (sku_or_None, match_note).
    Match priority:
      1. Exact match on product_name
      2. Exact match on raw original name/company string
      3. Brand + 'pen' shorthand (for pens where only brand was written)
      4. Partial: product_name substring appears in an inventory name
    """
    candidates = [
        product_name.strip().lower(),
        raw_name.strip().lower(),
        (brand.lower() + " pen") if brand else None,
        (brand.lower()) if brand else None,
    ]

    for candidate in candidates:
        if candidate and candidate in sku_lookup:
            return sku_lookup[candidate], "exact"

    # Partial substring match
    pn = product_name.strip().lower()
    if pn:
        for inv_name, sku in sku_lookup.items():
            if pn in inv_name or inv_name in pn:
                return sku, f"partial → '{inv_name}'"

    return None, None


def generate_sku(inv_df, category, subcategory):
    """Generate next sequential SKU for given category + subcategory."""
    cat_code = CATEGORY_CODES.get(category, "XX")
    sub_code = SUBCATEGORY_CODES.get(subcategory, "UNK")
    prefix   = f"{cat_code}-{sub_code}-"

    existing = inv_df[inv_df['SKU Code'].astype(str).str.startswith(prefix)]['SKU Code']
    if existing.empty:
        next_num = 1
    else:
        serials = (
            existing
            .str.replace(prefix, '', regex=False)
            .str.extract(r'^(\d+)$')[0]
        )
        serials = pd.to_numeric(serials, errors='coerce').dropna()
        next_num = int(serials.max()) + 1 if not serials.empty else 1

    return f"{prefix}{str(next_num).zfill(3)}"


def load_existing_sales(filepath):
    """Load existing Sales_Data.csv if it exists — returns set of Sl No already processed."""
    if os.path.exists(filepath):
        try:
            existing = pd.read_csv(filepath)
            if 'Sl No' in existing.columns:
                return set(existing['Sl No'].dropna().astype(int).tolist()), existing
        except Exception:
            pass
    return set(), pd.DataFrame()


# ═════════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════════

def main():
    print("=" * 62)
    print("  Om Stationeries — Sales & Inventory Processor")
    print(f"  {datetime.now().strftime('%d-%m-%Y  %H:%M')}")
    print("=" * 62)

    # Check files exist  
    for f in [SALES_ENTRY_FILE, INVENTORY_FILE]:
        if not os.path.exists(f):
            print(f"\n  ERROR: '{f}' not found.")
            print(f"  Make sure it is in the same folder as this script.")
            sys.exit(1)

    # Load  
    entry = pd.read_csv(SALES_ENTRY_FILE)
    inv   = pd.read_csv(INVENTORY_FILE)

    # Strip whitespace from column names
    entry.columns = entry.columns.str.strip()
    inv.columns   = inv.columns.str.strip()

    print(f"\n  Loaded Sales_Data_Entry : {len(entry)} rows")
    print(f"  Loaded Inventory_Data   : {len(inv)} rows")

    # Remove #DIV/0! and fully empty rows from entry
    entry = entry[~entry.apply(
        lambda r: r.astype(str).str.contains('#DIV/0!').any(), axis=1
    )]
    entry = entry.dropna(how='all').reset_index(drop=True)

    #  Load existing Sales_Data to avoid reprocessing 
    already_processed, existing_sales_df = load_existing_sales(SALES_OUTPUT_FILE)

    # Identify Sl No column (handle slight naming variations)
    sl_col = next((c for c in entry.columns if c.lower().replace(' ','').replace('_','') in ('slno','slno.')), None)
    if sl_col is None:
        print("\n  ERROR: Cannot find 'Sl no' column in Sales_Data_Entry.csv")
        sys.exit(1)

    # Filter to only new rows
    entry[sl_col] = pd.to_numeric(entry[sl_col], errors='coerce')
    new_rows = entry[~entry[sl_col].isin(already_processed)].copy()

    print(f"  Already in Sales_Data   : {len(already_processed)} rows")
    print(f"  New rows to process     : {len(new_rows)}")

    if new_rows.empty:
        print("\n  Nothing new to process. Add rows to Sales_Data_Entry and re-run.")
        sys.exit(0)

    # Identify columns  
    # Flexible column name matching
    def find_col(df, *hints):
        for h in hints:
            for c in df.columns:
                if h.lower() in c.lower():
                    return c
        return None

    date_col    = find_col(entry, 'date')
    time_col    = find_col(entry, 'time')
    subcat_col  = find_col(entry, 'sub', 'category')   # the raw "Sub-category" from entry
    name_col    = find_col(entry, 'name', 'company')
    rate_col    = find_col(entry, 'rate')
    qty_col     = find_col(entry, 'qty')
    cost_col    = find_col(entry, 'cost')
    payment_col = find_col(entry, 'mode', 'payment')

    missing = [label for label, col in [
        ('Date', date_col), ('Name/company', name_col),
        ('Rate', rate_col), ('Qty', qty_col), ('Cost', cost_col),
    ] if col is None]
    if missing:
        print(f"\n  ERROR: Cannot find columns: {missing}")
        print(f"  Found columns: {entry.columns.tolist()}")
        sys.exit(1)

    # Build SKU lookup 
    sku_lookup = build_sku_lookup(inv)

    # Process each new row
    print(f"\n{'─'*62}")
    print("  SCRIPT 1 — Processing Sales_Data_Entry")
    print(f"{'─'*62}")

    output_rows   = []
    no_sku_items  = []   # (sl_no, raw_name, brand, product_name) for Script 2
    review_count  = 0
    mapped_count  = 0

    for _, row in new_rows.iterrows():
        sl_no    = int(row[sl_col]) if pd.notna(row[sl_col]) else ''
        raw_date = str(row[date_col]).strip() if date_col else ''
        time_val = str(row[time_col]).strip() if time_col else ''
        raw_name = str(row[name_col]).strip() if name_col else ''
        rate     = row[rate_col] if rate_col else ''
        qty      = row[qty_col]  if qty_col  else ''
        cost     = row[cost_col] if cost_col else ''
        payment  = str(row[payment_col]).strip() if payment_col else ''

        # 1. Standardise date
        std_date = standardise_date(raw_date)

        # 2. Split brand / product name
        brand, product_name, needs_brand_review = split_brand_product(raw_name)

        # 3. Look up SKU
        sku, match_note = find_sku(product_name, brand, raw_name, sku_lookup)

        # 4. Determine review flag
        if sku is None:
            needs_review   = "⚠ NO SKU — run script again after inventory update"
            mapped_count_delta = 0
            no_sku_items.append((sl_no, raw_name, brand, product_name))
            print(f"  ⚠  Sl#{sl_no:>3}  '{raw_name}'  → NO SKU FOUND")
        elif needs_brand_review:
            needs_review   = "⚠ Brand unclear — verify Brand & Product Name"
            mapped_count  += 1
            print(f"  ?  Sl#{sl_no:>3}  '{raw_name}'  → {sku}  (brand unclear)")
        else:
            needs_review   = ""
            mapped_count  += 1
            if match_note and match_note != "exact":
                print(f"  ~  Sl#{sl_no:>3}  '{raw_name}'  → {sku}  ({match_note})")

        if needs_review:
            review_count += 1

        output_rows.append({
            'Sl No':             sl_no,
            'Date':              std_date,
            'Time':              time_val,
            'Brand':             brand,
            'Product Name':      product_name,
            'SKU':               sku if sku else "NOT MAPPED",
            'Rate (₹)':          rate,
            'Qty':               qty,
            'Cost (₹)':          cost,
            'Mode of Payment':   payment,
            'Needs Review':      needs_review,
        })

    # Combine with existing Sales_Data
    new_sales_df = pd.DataFrame(output_rows)
    if not existing_sales_df.empty:
        combined_sales = pd.concat([existing_sales_df, new_sales_df], ignore_index=True)
    else:
        combined_sales = new_sales_df

    combined_sales.to_csv(SALES_OUTPUT_FILE, index=False)

    print(f"\n  Result: {len(new_rows)} rows processed")
    print(f"    SKU mapped       : {mapped_count}")
    print(f"    Needs review     : {review_count}")
    print(f"    No SKU found     : {len(no_sku_items)}")
    print(f"\n  ✅ Saved: {SALES_OUTPUT_FILE}  ({len(combined_sales)} total rows)")

    # SCRIPT 2 — Add new SKUs to Inventory 
    print(f"\n{'─'*62}")
    print("  SCRIPT 2 — Updating Inventory_Data for unmatched items")
    print(f"{'─'*62}")

    if not no_sku_items:
        print("  Nothing to add — all sales rows had matching SKUs.")
    else:
        print(f"\n  Adding {len(no_sku_items)} new skeleton row(s) to Inventory_Data:\n")
        print("  ┌ ─────────────┐")
        print("  │  ⚠  FILL IN THESE ROWS IN Inventory_Data.csv        │")
        print("  │     Category, Sub-category, Rate, Qty, Cost Price   │")
        print("  └ ─────────────┘\n")

        new_inv_rows = []
        next_sl = int(inv['SL No'].max()) + 1 if 'SL No' in inv.columns else len(inv) + 1

        for sl_no, raw_name, brand, product_name in no_sku_items:
            # Build a readable name: prefer "Brand ProductName", fallback to raw
            inv_name = clean_inv_name(brand, product_name, raw_name)

            # Generate SKU under UNKNOWN/UNKNOWN
            new_sku = generate_sku(inv, "UNKNOWN", "UNKNOWN")

            new_row = {
                'SL No':               next_sl,
                'SKU Code':            new_sku,
                'Category':            'UNKNOWN',
                'Sub-category':        'UNKNOWN',
                'Name':                inv_name,
                'Unit of Measurement': '',
                'Rate':                '',
                'Qty':                 '',
                'Cost Price':          '',
            }
            new_inv_rows.append(new_row)

            # Also update SKU in the sales output now that we have it
            combined_sales.loc[
                (combined_sales['SKU'] == 'NOT MAPPED') &
                (combined_sales['Product Name'].str.strip().str.lower() == product_name.strip().lower()),
                'SKU'
            ] = new_sku

            # Add to lookup so subsequent rows in same batch can match it
            sku_lookup[inv_name.lower()] = new_sku

            # Append to inv df so generate_sku counter stays correct
            inv = pd.concat([inv, pd.DataFrame([new_row])], ignore_index=True)
            next_sl += 1

            print(f"  + {new_sku}  |  '{inv_name}'")
            print(f"    ↳ Sales row Sl#{sl_no} — original entry: '{raw_name}'")
            print()

        # Save updated inventory
        inv.to_csv(INVENTORY_FILE, index=False)
        print(f"  ✅ Saved: {INVENTORY_FILE}  ({len(inv)} rows)")

        # Re-save sales with updated SKUs
        combined_sales.to_csv(SALES_OUTPUT_FILE, index=False)
        print(f"  ✅ Updated: {SALES_OUTPUT_FILE} with new SKU codes")

    # ── FINAL SUMMARY  ─────
    print(f"\n{'═'*62}")
    print("  DONE")
    print(f"{'═'*62}")
    print(f"  Sales_Data.csv    : {len(combined_sales)} rows total")
    print(f"  Inventory_Data.csv: {len(inv)} rows total")

    still_unmapped = (combined_sales['SKU'] == 'NOT MAPPED').sum()
    still_review   = (combined_sales['Needs Review'] != '').sum()

    if still_unmapped == 0 and still_review == 0:
        print("\n  ✓  All rows clean — no action required.")
    else:
        print(f"\n  ⚠  ACTION REQUIRED IN Sales_Data.csv:")
        if still_unmapped > 0:
            print(f"     • {still_unmapped} row(s) still show 'NOT MAPPED' in SKU column")
        if still_review > 0:
            print(f"     • {still_review} row(s) flagged in 'Needs Review' column")
        print()
        print("  ⚠  ACTION REQUIRED IN Inventory_Data.csv:")
        unknown_rows = inv[inv['Category'] == 'UNKNOWN']
        if not unknown_rows.empty:
            print(f"     • {len(unknown_rows)} row(s) with Category = UNKNOWN need filling:")
            for _, r in unknown_rows.iterrows():
                print(f"       - {r['SKU Code']}  |  {r['Name']}")

    print(f"\n  {datetime.now().strftime('%H:%M:%S')}  Complete.")
    print("=" * 62)


if __name__ == "__main__":
    main()
