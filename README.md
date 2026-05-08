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


## Data Handling

- Raw ledger entries were digitised and processed through a four-stage Python pipeline
- Ambiguous product names were resolved via alias matching and manual verification. Stock quantities are owner-stated estimates and are acknowledged as a limitation throughout.

---

## Methods of Analysis

- **Margin analysis**
- **Strategic quadrant analysis**
- **ABC classification**
- **Velocity analysis**
- **Time-of-day analysis**

---
## Outcomes

Data revealed that 24.2% of SKUs fall below the 20% margin threshold, with Writing Instruments and Toys & Games most at risk. Just 43 SKUs drive 70% of total revenue, while several categories — notably Files & Folders and School Supplies — hold hundreds of days of excess stock. The project delivers tiered restocking guidelines, targeted pricing recommendations, and a lightweight daily logging habit that gives the owner an ongoing data foundation without disrupting store operations. Study under BDM Capstone Project, IIT Madras

---

## Repository Structure
```
├── LICENSE
├── Insights.pdf
└── README.md
```
[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)
**BDM Capstone Project — IIT Madras | Author: Sinchana V**
