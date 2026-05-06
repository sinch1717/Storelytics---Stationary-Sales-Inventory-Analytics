"""
SCRIPT 3 — SKU CODE GENERATION
Auto-generates SKU codes in format: CAT-SUB-001
Input:  inventory_step2_uom.csv
Output: inventory_step3_sku.csv  ← YOUR FINAL INVENTORY FILE
"""

import pandas as pd
import re

df = pd.read_csv("inventory_step2_uom.csv")
print(f"Rows loaded: {len(df)}")

 
# CATEGORY CODE MAP (2-letter codes)
 

category_codes = {
    "Writing Instruments":          "WI",
    "Paper Products":               "PP",
    "Files and Folders":            "FF",
    "Office Desk Supplies":         "OD",
    "Adhesives & Tapes":            "AT",
    "Correction & Erasing Items":   "CE",
    "Measurement & Geometry Tools": "MG",
    "Art & Craft Supplies":         "AC",
    "School-Specific Supplies":     "SS",
    "Office Forms & Registers":     "OF",
    "Printing & Computer Stationery": "PC",
    "Fasteners & Binding Materials":"FB",
    "Envelopes & Mailing Supplies": "EM",
    "Miscellaneous / Utility Items":"MU",
    "Toys & Games":                 "TG",
    "Electronics & Accessories":    "EL",
    "Services":                     "SV",
}

 
# EXPLICIT SUB-CATEGORY CODE MAP (3-letter codes)
# These are hand-defined to ensure uniqueness and readability.
 

subcategory_codes = {
    # Writing Instruments
    "Pens":                                         "PEN",
    "Pencils":                                      "PCL",
    "Markers":                                      "MRK",
    "Highlighters":                                 "HLT",
    "Sketching & Colour Writing":                   "SKC",
    "Chalk & Board Writing":                        "CBW",
    "Erasing & Correction for Writing Instruments": "ERC",
    "Sharpening & Pencil Maintenance":              "SHP",
    "Accessories for Writing Instruments":          "AWI",

    # Paper Products
    "Notebooks & Writing Books":                    "NWB",
    "Registers & Office Books":                     "ROB",
    "Loose Writing Paper":                          "LWP",
    "Printing & Copier Paper":                      "PCP",
    "Drawing & Art Paper":                          "DAP",
    "Craft & Decorative Paper":                     "CDP",
    "Card & Board Paper":                           "CBP",
    "Technical & Specialty Paper":                  "TSP",
    "Sticky & Label Paper":                         "SLP",
    "Envelopes & Mailing Paper":                    "EMP",
    "Diaries & Planners":                           "DPL",
    "Academic & Exam Paper":                        "AEP",
    "Packaging & Wrapping Paper":                   "PWP",
    "Rolls & Large Format Paper":                   "RLF",

    # Files and Folders
    "Basic Files":                                  "BFL",
    "Plastic Files":                                "PLF",
    "Display & Presentation Files":                 "DPF",
    "Ring Binder Files":                            "RBF",
    "Lever Arch & Office Files":                    "LAF",
    "Expanding Files":                              "EXF",
    "Box & Storage Files":                          "BSF",
    "Academic / Project Files":                     "APF",
    "Legal & Government Files":                     "LGF",
    "File Accessories":                             "FAC",

    # Office Desk Supplies
    "Stapling Supplies":                            "STS",
    "Pinning Supplies":                             "PIN",
    "Punching Tools":                               "PUN",
    "Cutting Tools":                                "CUT",
    "Clipping & Fastening":                         "CLF",
    "Adhesive Handling":                            "ADH",
    "Measuring Tools":                              "MST",
    "Desk Organization":                            "DSO",
    "Display & Desk Items":                         "DDI",
    "Miscellaneous Desk Items":                     "MDI",

    # Adhesives & Tapes
    "Liquid Adhesives":                             "LQA",
    "Glue Sticks":                                  "GLS",
    "Instant Adhesives":                            "INS",
    "Industrial / Strong Adhesives":                "ISA",
    "Tape Types":                                   "TAP",
    "Specialty Tapes":                              "SPT",
    "Glue Application Tools":                       "GAT",
    "Adhesive Accessories":                         "AAC",

    # Correction & Erasing
    "Erasers":                                      "ERS",
    "Correction Fluids":                            "CFL",
    "Correction Pens":                              "CPE",
    "Correction Tapes":                             "CTP",
    "Specialty Correction Supplies":                "SCS",
    "Erasing Devices":                              "ERD",

    # Measurement & Geometry
    "Rulers & Scales":                              "RLS",
    "Compasses":                                    "CMP",
    "Dividers":                                     "DIV",
    "Protractors":                                  "PRO",
    "Set Squares":                                  "SSQ",
    "Geometry Sets / Boxes":                        "GEO",
    "Measuring Instruments":                        "MIN",
    "Drafting Tools":                               "DFT",
    "Accessories":                                  "ACC",

    # Art & Craft
    "Colouring Supplies":                           "COL",
    "Paints":                                       "PNT",
    "Brushes":                                      "BRS",
    "Drawing Materials":                            "DRM",
    "Craft Papers & Sheets":                        "CPS",
    "Craft Decoration Materials":                   "CDM",
    "Clay & Modelling":                             "CLY",
    "Cutting & Craft Tools":                        "CCT",
    "Adhesives for Craft":                          "AFC",
    "Painting Surfaces":                            "PAS",
    "DIY & Craft Kits":                             "DIY",
    "Board & Sheet Materials":                      "BSM",
    "Specialty Craft Materials":                    "SCM",

    # School-Specific
    "Writing & Study Essentials":                   "WSE",
    "School Bags & Carry Items":                    "SBC",
    "Identification & Labels":                      "IDL",
    "Book Protection":                              "BKP",
    "Learning Tools":                               "LTL",
    "Exam & Academic Supplies":                     "EAS",
    "Diaries & School Records":                     "DSR",
    "Student Accessories":                          "STA",

    # Office Forms & Registers
    "Accounting Registers":                         "ACR",
    "Attendance & Staff Records":                   "ASR",
    "Inventory & Stock Records":                    "ISR",
    "Billing & Transaction Books":                  "BTB",
    "Receipt & Payment Records":                    "RPR",
    "Order & Dispatch Records":                     "ODR",
    "Administrative Records":                       "ADR",
    "Pre-Printed Office Forms":                     "PPF",
    "Miscellaneous Office Books":                   "MOB",

    # Printing & Computer Stationery
    "Copier & Printer Paper":                       "CPP",
    "Photo & Specialty Printing Paper":             "PSP",
    "Label & Sticker Sheets":                       "LSS",
    "Continuous & Dot Matrix Paper":                "CDM",  # note: CDM also used in Art - both fine as cat prefix differs
    "Billing & Thermal Paper":                      "BTP",
    "Printer Consumables":                          "PRC",
    "Data Storage Media":                           "DSM",
    "Computer Forms & Sheets":                      "CFS",
    "Large Format Printing":                        "LFP",
    "Finishing & Binding Supplies":                 "FBS",

    # Fasteners & Binding
    "Paper Fasteners":                              "PAF",
    "Pin & Tag Fasteners":                          "PTF",
    "Metal Fasteners":                              "MTF",
    "Elastic Fasteners":                            "ELF",
    "Binder Rings":                                 "BNR",
    "Spiral Binding Materials":                     "SBM",
    "Comb Binding Materials":                       "CBM",
    "Thermal Binding Materials":                    "TBM",
    "File Binding Materials":                       "FBM",
    "Lamination & Finishing Materials":             "LFM",

    # Envelopes & Mailing
    "Paper Envelopes":                              "PEN",
    "Brown Envelopes":                              "BEN",
    "Window Envelopes":                             "WEN",
    "Invitation & Greeting Envelopes":              "IGE",
    "Security Envelopes":                           "SEC",
    "Courier & Shipping Envelopes":                 "CSE",
    "Bubble & Protective Mailers":                  "BPM",
    "Interoffice Mail Supplies":                    "IMS",
    "Packaging Paper":                              "PKP",
    "Addressing Supplies":                          "ADS",
    "Sealing Supplies":                             "SEL",

    # Miscellaneous / Utility
    "Calculators":                                  "CAL",
    "Boards & Display Items":                       "BDI",
    "Board Accessories":                            "BAC",
    "Desk Display Items":                           "DDT",
    "Sealing & Stamping Items":                     "SSI",
    "Identification & Tags":                        "IDT",
    "Miscellaneous Office Tools":                   "MOT",

    # Toys & Games
    "Die-Cast & Model Vehicles":                    "DMV",
    "Puzzle & Strategy Games":                      "PSG",
    "Action & Soft Toys":                           "AST",
    "Sports Toys":                                  "SPO",

    # Electronics & Accessories
    "Storage Devices":                              "SDE",
    "Cables & Connectors":                          "CAB",
    "Audio":                                        "AUD",
    "Input Devices":                                "INP",
    "Batteries":                                    "BAT",
    "Laser & Light Accessories":                    "LLA",
    "Printer Consumables (Electronics)":            "PCE",

    # Services
    "Reprographics":                                "RPG",
    "Printing":                                     "PRT",
    "Courier":                                      "COU",
}

 
# FALLBACK: Auto-generate 3-letter code from sub-category name
# Used only if a sub-category is not in the explicit map above
 
def auto_subcat_code(subcategory):
    words = re.findall(r'\b[A-Za-z]', subcategory)
    if len(words) >= 3:
        return "".join(words[:3]).upper()
    elif len(words) == 2:
        return (words[0] + words[1] + subcategory.replace(" ", "")[2]).upper()
    else:
        return subcategory[:3].upper()

 
# GENERATE SKU CODES
 

counters = {}  # tracks serial per CAT-SUB combo
skus = []
unmapped_cats = set()
unmapped_subcats = set()

for _, row in df.iterrows():
    cat = str(row["Category"]).strip()
    subcat = str(row["Sub-category"]).strip()

    cat_code = category_codes.get(cat)
    if not cat_code:
        cat_code = cat[:2].upper()
        unmapped_cats.add(cat)

    subcat_code = subcategory_codes.get(subcat)
    if not subcat_code:
        subcat_code = auto_subcat_code(subcat)
        unmapped_subcats.add(subcat)

    key = f"{cat_code}-{subcat_code}"
    counters[key] = counters.get(key, 0) + 1
    serial = str(counters[key]).zfill(3)

    skus.append(f"{cat_code}-{subcat_code}-{serial}")

df["SKU Code"] = skus

 
# REPORT

if unmapped_cats:
    print(f"\nCategories not in map (used first 2 chars as fallback):")
    for c in unmapped_cats:
        print(f"  - {c}")

if unmapped_subcats:
    print(f"\nSub-categories not in map (used auto-generated code):")
    for s in unmapped_subcats:
        print(f"  - {s}")

print(f"\n✅ SKU codes generated for all {len(df)} rows.")
print("\nSample SKUs:")
print(df[["SKU Code", "Category", "Sub-category", "Name"]].head(20).to_string(index=False))

 
# SAVE FINAL OUTPUT
 

# Reorder columns cleanly
cols = ["SL No", "SKU Code", "Category", "Sub-category", "Name",
        "Unit of Measurement", "Rate", "Qty", "Cost Price"]
# Only include columns that exist
cols = [c for c in cols if c in df.columns]
df = df[cols]

df.to_csv("inventory_step3_sku.csv", index=False)
print("\n✅ Saved: inventory_step3_sku.csv  ← Your final inventory file")
print("   (Fill in Rate, Qty, and Cost Price manually in this file)")