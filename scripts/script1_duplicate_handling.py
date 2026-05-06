"""
SCRIPT 1 — DUPLICATE HANDLING
Removes duplicate entries from wrong categories and ensures
each item lives only in its correct category/sub-category.
Input:  BDM_Data_-_Inventory_Data.csv
Output: inventory_step1_deduped.csv
"""

import pandas as pd

df = pd.read_csv("BDM_Data_-_Inventory_Data.csv")
print(f"Original row count: {len(df)}")

 
# DUPLICATE REMOVAL RULES
# Format: (item_name, category_to_DELETE_from, sub_category_to_DELETE_from)
# The correct copy (in the right category) is KEPT untouched.
 

removal_rules = [

    # Glue guns & sticks → keep in Art & Craft, delete from Adhesives & Tapes
    ("Glue guns",               "Adhesives & Tapes",        "Glue Application Tools"),
    ("Glue gun sticks",         "Adhesives & Tapes",        "Glue Application Tools"),

    # Tape dispensers → keep in Office Desk Supplies, delete from Adhesives & Tapes
    ("Tape dispensers",         "Adhesives & Tapes",        "Adhesive Accessories"),

    # Pins → keep in Fasteners & Binding, delete from Office Desk Supplies & Measurement & Geometry
    ("Drawing pins",            "Office Desk Supplies",     "Pinning Supplies"),
    ("Drawing pins",            "Measurement & Geometry Tools", "Accessories"),
    ("Push pins",               "Office Desk Supplies",     "Pinning Supplies"),
    ("Thumb pins",              "Office Desk Supplies",     "Pinning Supplies"),
    ("Map pins",                "Office Desk Supplies",     "Pinning Supplies"),
    ("T-pins",                  "Office Desk Supplies",     "Pinning Supplies"),

    # Clips → keep in Fasteners & Binding, delete from Office Desk Supplies
    ("Paper clips",             "Office Desk Supplies",     "Clipping & Fastening"),
    ("Binder clips",            "Office Desk Supplies",     "Clipping & Fastening"),
    ("Bulldog clips",           "Office Desk Supplies",     "Clipping & Fastening"),
    ("Foldback clips",          "Office Desk Supplies",     "Clipping & Fastening"),
    ("Gem clips",               "Office Desk Supplies",     "Clipping & Fastening"),
    ("Rubber bands",            "Office Desk Supplies",     "Clipping & Fastening"),
    ("Brass fasteners",         "Office Desk Supplies",     "Clipping & Fastening"),
    ("Split pins",              "Office Desk Supplies",     "Clipping & Fastening"),
    ("Paper fasteners",         "Office Desk Supplies",     "Clipping & Fastening"),

    # Pen stands → keep in Office Desk Supplies, delete from Writing Instruments
    ("Pen stands",              "Writing Instruments",      "Accessories for Writing Instruments"),

    # Magazine holders → keep in Office Desk Supplies, delete from Files and Folders
    ("Magazine holders",        "Files and Folders",        "Box & Storage Files"),

    # Ink bottles → keep in Writing Instruments, delete from Office Desk Supplies
    ("Ink bottles",             "Office Desk Supplies",     "Miscellaneous Desk Items"),

    # Erasers & correction → keep in Correction & Erasing Items, delete from Writing Instruments
    ("Pencil erasers",          "Writing Instruments",      "Erasing & Correction for Writing Instruments"),
    ("Kneaded erasers",         "Writing Instruments",      "Erasing & Correction for Writing Instruments"),
    ("Electric erasers",        "Writing Instruments",      "Erasing & Correction for Writing Instruments"),
    ("Correction fluid",        "Writing Instruments",      "Erasing & Correction for Writing Instruments"),
    ("Correction tape",         "Writing Instruments",      "Erasing & Correction for Writing Instruments"),

    # Art materials → keep in Art & Craft, delete from Writing Instruments
    ("Graphite sticks",         "Writing Instruments",      "Pencils"),
    ("Charcoal pencils",        "Writing Instruments",      "Pencils"),
    ("Colour pencils",          "Writing Instruments",      "Pencils"),  # listed as "Coloured pencils"
    ("Coloured pencils",        "Writing Instruments",      "Pencils"),
    ("Watercolour pencils",     "Writing Instruments",      "Pencils"),

    # Whiteboard markers → keep in Miscellaneous / Utility, delete from Writing Instruments
    ("Whiteboard markers",      "Writing Instruments",      "Markers"),

    # Copier/printer paper → keep in Printing & Computer Stationery, delete from Paper Products
    ("A4 copier paper",         "Paper Products",           "Printing & Copier Paper"),
    ("A3 paper",                "Paper Products",           "Printing & Copier Paper"),
    ("Legal size paper",        "Paper Products",           "Printing & Copier Paper"),
    ("Letter size paper",       "Paper Products",           "Printing & Copier Paper"),
    ("Executive size paper",    "Paper Products",           "Printing & Copier Paper"),
    ("Bond paper",              "Paper Products",           "Printing & Copier Paper"),
    ("Maplitho paper",          "Paper Products",           "Printing & Copier Paper"),
    ("Multipurpose printer paper", "Paper Products",        "Printing & Copier Paper"),
    ("Colour printing paper",   "Paper Products",           "Printing & Copier Paper"),
    ("Plotter paper rolls",     "Paper Products",           "Rolls & Large Format Paper"),
    ("CAD paper rolls",         "Paper Products",           "Rolls & Large Format Paper"),

    # Lamination & binding → keep in Printing & Computer Stationery, delete from Fasteners & Binding
    ("Lamination pouches",      "Fasteners & Binding Materials", "Lamination & Finishing Materials"),
    ("Lamination rolls",        "Fasteners & Binding Materials", "Lamination & Finishing Materials"),
    ("Spiral binding covers (plastic)", "Fasteners & Binding Materials", "Spiral Binding Materials"),

    # Craft papers → keep in Art & Craft, delete from Paper Products
    ("Craft paper",             "Paper Products",           "Craft & Decorative Paper"),
    ("Glitter paper",           "Paper Products",           "Craft & Decorative Paper"),
    ("Metallic paper",          "Paper Products",           "Craft & Decorative Paper"),
    ("Origami paper",           "Paper Products",           "Craft & Decorative Paper"),
    ("Handmade paper",          "Paper Products",           "Craft & Decorative Paper"),

    # Geometry & compass boxes → keep in Measurement & Geometry, delete from School-Specific
    ("Geometry boxes",          "School-Specific Supplies", "Student Accessories"),
    ("Compass boxes",           "School-Specific Supplies", "Student Accessories"),

    # Project & assignment files → keep in Files and Folders, delete from School-Specific & Office Forms
    ("Project files",           "School-Specific Supplies", "Exam & Academic Supplies"),
    ("Project files",           "Office Forms & Registers", "Administrative Records"),  # if exists
    ("Assignment files",        "School-Specific Supplies", "Exam & Academic Supplies"),

    # Answer/supplement sheets → keep in School-Specific, delete from Paper Products
    ("Answer sheets",           "Paper Products",           "Academic & Exam Paper"),
    ("Supplement sheets",       "Paper Products",           "Academic & Exam Paper"),

    # Office registers → keep in Office Forms & Registers, delete from Paper Products
    ("Ledger books",            "Paper Products",           "Registers & Office Books"),
    ("Cash books",              "Paper Products",           "Registers & Office Books"),
    ("Attendance registers",    "Paper Products",           "Registers & Office Books"),
    ("Stock registers",         "Paper Products",           "Registers & Office Books"),
    ("Visitor registers",       "Paper Products",           "Registers & Office Books"),
    ("Dispatch registers",      "Paper Products",           "Registers & Office Books"),
    ("Order registers",         "Paper Products",           "Registers & Office Books"),
    ("Complaint registers",     "Paper Products",           "Registers & Office Books"),
]

 
# APPLY REMOVALS
 

removed_log = []

for (name, wrong_category, wrong_subcategory) in removal_rules:
    mask = (
        (df["Name"].str.strip().str.lower() == name.strip().lower()) &
        (df["Category"].str.strip() == wrong_category.strip()) &
        (df["Sub-category"].str.strip() == wrong_subcategory.strip())
    )
    matched = df[mask]
    if not matched.empty:
        removed_log.append({
            "Name": name,
            "Removed from Category": wrong_category,
            "Removed from Sub-category": wrong_subcategory,
            "Rows removed": len(matched)
        })
        df = df[~mask]
    else:
        # Try a looser match on just name + category (sub-category naming may differ slightly)
        mask_loose = (
            (df["Name"].str.strip().str.lower() == name.strip().lower()) &
            (df["Category"].str.strip() == wrong_category.strip())
        )
        matched_loose = df[mask_loose]
        if not matched_loose.empty:
            removed_log.append({
                "Name": name,
                "Removed from Category": wrong_category,
                "Removed from Sub-category": f"(loose match) {matched_loose['Sub-category'].values[0]}",
                "Rows removed": len(matched_loose)
            })
            df = df[~mask_loose]

 
# RESET SL No AFTER DELETIONS

df = df.reset_index(drop=True)
df["SL No"] = df.index + 1

 
# SAVE OUTPUT
 

df.to_csv("inventory_step1_deduped.csv", index=False)

print(f"Rows after deduplication: {len(df)}")
print(f"Total duplicates removed: {sum(r['Rows removed'] for r in removed_log)}")
print("\n--- Removal Log ---")
for r in removed_log:
    print(f"  REMOVED: '{r['Name']}' from [{r['Removed from Category']}] → [{r['Removed from Sub-category']}]  ({r['Rows removed']} row/s)")

not_found = [r for r in removal_rules if r[0] not in [l['Name'] for l in removed_log]]
if not_found:
    print(f"\n⚠ These items were NOT found (may already be clean or name mismatch):")
    for n in not_found:
        print(f"  - '{n[0]}' in [{n[1]}]")

print("\n Saved: inventory_step1_deduped.csv")