# Storelytics---Stationary-Sales-Inventory-Analytics
## Enhancing Sales Visibility and Inventory Decision-Making in a Small Retail Stationery Business
Enhancing Sales Visibility and Inventory Decision-Making in a Small Retail Stationery Business

Om Stationeries is a small neighbourhood retail shop in Dattagalli, Mysuru, operating across 17 product categories with 664 SKUs. This project digitises and analyses 29 days of sales and inventory data to surface pricing gaps, inventory inefficiencies, and operational patterns — replacing owner intuition with structured, data-backed decisions.

---

## Problem Statement

The business faced three major operational challenges:

**PS1 – Profitability Visibility**
The owner assumed a uniform gross margin of 15–20% across products, but there was no structured mechanism to verify actual margins.

**PS2 – Inventory Movement**
Restocking decisions relied entirely on visual judgement, with no data identifying fast-moving products, slow-moving products, capital lock-in, or stock velocity.

**PS3 – Experience vs Data**
All decisions depended on owner memory and intuition, without historical records to validate operational assumptions.

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Google Colab](https://img.shields.io/badge/Google%20Colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=python&logoColor=white)
![Google Sheets](https://img.shields.io/badge/Google%20Sheets-34A853?style=for-the-badge&logo=googlesheets&logoColor=white)

---

## Product Categories

| Code | Category |
|------|----------|
| WI | Writing Instruments |
| PP | Paper Products |
| FF | Files and Folders |
| OD | Office Desk Supplies |
| AT | Adhesives & Tapes |
| CE | Correction & Erasing Items |
| MG | Measurement & Geometry Tools |
| AC | Art & Craft Supplies |
| SS | School-Specific Supplies |
| OF | Office Forms & Registers |
| PC | Printing & Computer Stationery |
| FB | Fasteners & Binding Materials |
| EM | Envelopes & Mailing Supplies |
| MU | Miscellaneous / Utility Items |
| TG | Toys & Games |
| EL | Electronics & Accessories |
| SV | Services |

---

## Data Handling

Raw ledger entries were digitised and processed through a four-stage Python pipeline:

| Script | Purpose |
|--------|---------|
| `script1_duplicate_handling.py` | Deduplication & category mapping |
| `script2_uom.py` | Unit of measurement assignment |
| `script3_sku.py` | SKU code generation |
| `om_stationeries.py` | Sales processing pipeline |

**SKU Format:** `[CATEGORY CODE]-[SUBCATEGORY CODE]-[SEQUENCE]` — e.g. `WI-PEN-011`

Ambiguous product names were resolved via alias matching and manual verification. Stock quantities are owner-stated estimates and are acknowledged as a limitation throughout.

---

## Methods of Analysis

- **Margin analysis** — Gross margin distribution across SKUs and categories; compared against the owner's assumed 15–20% floor
- **Strategic quadrant analysis** — Categories plotted on margin % vs. revenue to identify Stars, Volume Risk, and Untapped segments
- **ABC classification** — SKUs ranked by revenue contribution into Tier A / B / C for inventory prioritisation
- **Velocity analysis** — Stock value vs. 29-day sales revenue per category to detect capital lock-in
- **Time-of-day analysis** — Transaction heatmap with coefficient of variation (CV) per slot to assess demand predictability

---

## Key Insights

**Margin Analysis**
- 24.2% of priced SKUs fall below the assumed 20% margin threshold
- Writing Instruments generated high revenue but operated at relatively lower margins
- Art & Craft Supplies emerged as the only high-revenue, high-margin "Star" category

**Inventory Analysis**
- 43 SKUs generated nearly 70% of total revenue
- Writing Instruments held ₹3.8L inventory at only 7% stock velocity
- Files & Folders showed extremely low movement relative to invested capital

**Operational Insights**
- Morning and Night sales slots were the most volatile
- Evening transactions were the most predictable operational window
- Several best-selling products operated below the margin floor

---

## Outcomes

Data revealed that 24.2% of SKUs fall below the 20% margin threshold, with Writing Instruments and Toys & Games most at risk. Just 43 SKUs drive 70% of total revenue, while several categories — notably Files & Folders and School Supplies — hold hundreds of days of excess stock. The project delivers tiered restocking guidelines, targeted pricing recommendations, and a lightweight daily logging habit that gives the owner an ongoing data foundation without disrupting store operations. Study under BDM Capstone Project, IIT Madras

---

## Repository Structure
```
├── notebooks/
│   ├── graphs.ipynb
├── scripts/
│   ├── script1_duplicate_handling.py
│   ├── script2_uom.py
│   ├── script3_sku.py
│   └── om_stationeries.py
├── Insights.pdf
└── README.md
```
**BDM Capstone Project — IIT Madras | Author: Sinchana V**
