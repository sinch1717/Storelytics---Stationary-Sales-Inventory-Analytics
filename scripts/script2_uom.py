"""
SCRIPT 2 — UNIT OF MEASUREMENT
Fills the 'Unit of Measurement' column based on Sub-category mapping.
Input:  inventory_step1_deduped.csv
Output: inventory_step2_uom.csv
"""

import pandas as pd

df = pd.read_csv("inventory_step1_deduped.csv")
print(f"Rows loaded: {len(df)}")

 
# SUB-CATEGORY → UOM MAPPING
 

uom_map = {
    # Writing Instruments
    "Pens":                                     "Piece",
    "Pen refills":                              "Piece",
    "Pencils":                                  "Piece",
    "Refill leads":                             "Pack",
    "Lead containers":                          "Piece",
    "Markers":                                  "Piece",
    "Highlighters":                             "Piece",
    "Sketching & Colour Writing":               "Piece",
    "Chalk & Board Writing":                    "Pack",
    "Erasing & Correction for Writing Instruments": "Piece",
    "Sharpening & Pencil Maintenance":          "Piece",
    "Accessories for Writing Instruments":      "Piece",
    "Ink bottles":                              "Bottle",
    "Ink converters":                           "Piece",
    "Cartridge ink packs":                      "Pack",

    # Paper Products
    "Notebooks & Writing Books":                "Piece",
    "Registers & Office Books":                 "Piece",
    "Loose Writing Paper":                      "Pack",
    "Printing & Copier Paper":                  "Ream",
    "Drawing & Art Paper":                      "Sheet",
    "Craft & Decorative Paper":                 "Sheet",
    "Card & Board Paper":                       "Sheet",
    "Technical & Specialty Paper":              "Sheet",
    "Sticky & Label Paper":                     "Pack",
    "Envelopes & Mailing Paper":                "Pack",
    "Diaries & Planners":                       "Piece",
    "Academic & Exam Paper":                    "Pack",
    "Packaging & Wrapping Paper":               "Roll",
    "Rolls & Large Format Paper":               "Roll",

    # Files and Folders
    "Basic Files":                              "Piece",
    "Plastic Files":                            "Piece",
    "Display & Presentation Files":             "Piece",
    "Ring Binder Files":                        "Piece",
    "Lever Arch & Office Files":                "Piece",
    "Expanding Files":                          "Piece",
    "Box & Storage Files":                      "Piece",
    "Academic / Project Files":                 "Piece",
    "Legal & Government Files":                 "Piece",
    "File Accessories":                         "Pack",

    # Office Desk Supplies
    "Stapling Supplies":                        "Piece",
    "Pinning Supplies":                         "Pack",
    "Punching Tools":                           "Piece",
    "Cutting Tools":                            "Piece",
    "Clipping & Fastening":                     "Pack",
    "Adhesive Handling":                        "Piece",
    "Measuring Tools":                          "Piece",
    "Desk Organization":                        "Piece",
    "Display & Desk Items":                     "Piece",
    "Miscellaneous Desk Items":                 "Piece",

    # Adhesives & Tapes
    "Liquid Adhesives":                         "Bottle",
    "Glue Sticks":                              "Piece",
    "Instant Adhesives":                        "Piece",
    "Industrial / Strong Adhesives":            "Piece",
    "Tape Types":                               "Roll",
    "Specialty Tapes":                          "Roll",
    "Glue Application Tools":                   "Piece",
    "Adhesive Accessories":                     "Piece",

    # Correction & Erasing Items
    "Erasers":                                  "Piece",
    "Correction Fluids":                        "Bottle",
    "Correction Pens":                          "Piece",
    "Correction Tapes":                         "Piece",
    "Specialty Correction Supplies":            "Piece",
    "Erasing Devices":                          "Piece",

    # Measurement & Geometry Tools
    "Rulers & Scales":                          "Piece",
    "Compasses":                                "Piece",
    "Dividers":                                 "Piece",
    "Protractors":                              "Piece",
    "Set Squares":                              "Piece",
    "Geometry Sets / Boxes":                    "Set",
    "Measuring Instruments":                    "Piece",
    "Drafting Tools":                           "Piece",
    "Accessories":                              "Piece",

    # Art & Craft Supplies
    "Colouring Supplies":                       "Set",
    "Paints":                                   "Bottle / Tube",
    "Brushes":                                  "Piece",
    "Drawing Materials":                        "Piece",
    "Craft Papers & Sheets":                    "Sheet",
    "Craft Decoration Materials":               "Pack",
    "Clay & Modelling":                         "Pack",
    "Cutting & Craft Tools":                    "Piece",
    "Adhesives for Craft":                      "Piece",
    "Painting Surfaces":                        "Piece",
    "DIY & Craft Kits":                         "Set",
    "Accessories":                              "Piece",
    "Board & Sheet Materials":                  "Sheet",
    "Specialty Craft Materials":                "Piece",

    # School-Specific Supplies
    "Writing & Study Essentials":               "Piece",
    "School Bags & Carry Items":                "Piece",
    "Identification & Labels":                  "Pack",
    "Book Protection":                          "Roll / Sheet",
    "Learning Tools":                           "Piece",
    "Exam & Academic Supplies":                 "Pack",
    "Diaries & School Records":                 "Piece",
    "Student Accessories":                      "Set",

    # Office Forms & Registers
    "Accounting Registers":                     "Piece",
    "Attendance & Staff Records":               "Piece",
    "Inventory & Stock Records":                "Piece",
    "Billing & Transaction Books":              "Piece",
    "Receipt & Payment Records":                "Piece",
    "Order & Dispatch Records":                 "Piece",
    "Administrative Records":                   "Piece",
    "Pre-Printed Office Forms":                 "Piece",
    "Miscellaneous Office Books":               "Piece",

    # Printing & Computer Stationery
    "Copier & Printer Paper":                   "Ream",
    "Photo & Specialty Printing Paper":         "Pack",
    "Label & Sticker Sheets":                   "Pack",
    "Continuous & Dot Matrix Paper":            "Pack",
    "Billing & Thermal Paper":                  "Roll",
    "Printer Consumables":                      "Piece / Bottle",
    "Data Storage Media":                       "Piece",
    "Computer Forms & Sheets":                  "Pack",
    "Large Format Printing":                    "Roll",
    "Finishing & Binding Supplies":             "Pack",

    # Fasteners & Binding Materials
    "Paper Fasteners":                          "Pack",
    "Pin & Tag Fasteners":                      "Pack",
    "Metal Fasteners":                          "Pack",
    "Elastic Fasteners":                        "Pack",
    "Binder Rings":                             "Pack",
    "Spiral Binding Materials":                 "Pack",
    "Comb Binding Materials":                   "Pack",
    "Thermal Binding Materials":                "Pack",
    "File Binding Materials":                   "Pack",
    "Lamination & Finishing Materials":         "Pack",

    # Envelopes & Mailing Supplies
    "Paper Envelopes":                          "Pack",
    "Brown Envelopes":                          "Pack",
    "Window Envelopes":                         "Pack",
    "Invitation & Greeting Envelopes":          "Pack",
    "Security Envelopes":                       "Pack",
    "Courier & Shipping Envelopes":             "Pack",
    "Bubble & Protective Mailers":              "Pack",
    "Interoffice Mail Supplies":                "Pack",
    "Packaging Paper":                          "Roll / Sheet",
    "Addressing Supplies":                      "Pack",
    "Sealing Supplies":                         "Piece / Roll",

    # Miscellaneous / Utility Items
    "Calculators":                              "Piece",
    "Boards & Display Items":                   "Piece",
    "Board Accessories":                        "Piece",
    "Desk Display Items":                       "Piece",
    "Sealing & Stamping Items":                 "Piece",
    "Identification & Tags":                    "Piece",
    "Miscellaneous Office Tools":               "Piece",

    # Toys & Games
    "Die-Cast & Model Vehicles":                "Piece",
    "Puzzle & Strategy Games":                  "Set",
    "Action & Soft Toys":                       "Piece",
    "Sports Toys":                              "Piece",

    # Electronics & Accessories
    "Storage Devices":                          "Piece",
    "Cables & Connectors":                      "Piece",
    "Audio":                                    "Piece",
    "Input Devices":                            "Piece",
    "Batteries":                                "Pack",
    "Laser & Light Accessories":                "Piece",
    "Printer Consumables (Electronics)":        "Bottle",

    # Services
    "Reprographics":                            "Per Transaction",
    "Printing":                                 "Per Transaction",
    "Courier":                                  "Per Transaction",
}

 
# APPLY UOM MAPPING
 

def get_uom(subcategory):
    subcategory = str(subcategory).strip()
    return uom_map.get(subcategory, "")

df["Unit of Measurement"] = df["Sub-category"].apply(get_uom)

 
# REPORT UNMAPPED SUB-CATEGORIES
 

unmapped = df[df["Unit of Measurement"] == ""]["Sub-category"].unique()
if len(unmapped) > 0:
    print(f"\n⚠ {len(unmapped)} sub-categories had no UOM mapping:")
    for u in unmapped:
        print(f"  - '{u}'")
else:
    print("✅ All sub-categories mapped successfully.")

filled = df[df["Unit of Measurement"] != ""].shape[0]
print(f"\nUOM filled for {filled} of {len(df)} rows.")

 
# SAVE OUTPUT
 

df.to_csv("inventory_step2_uom.csv", index=False)
print("✅ Saved: inventory_step2_uom.csv")