<p align="center">
  <img src="AdventureWorks%20Images/AdventureWorks_Logo.png" width="380" alt="AdventureWorks logo">
</p>

<h1 align="center">AdventureWorks Sales &amp; Customer Analytics</h1>
<p align="center"><b>An end-to-end Power BI project — from raw CSVs to an 8-page, AI-augmented business intelligence report.</b></p>

<p align="center">
  <img src="https://img.shields.io/badge/Power%20BI-Desktop-F2C811?style=flat-square&logo=powerbi&logoColor=black" alt="Power BI">
  <img src="https://img.shields.io/badge/DAX-Measures-20E2D7?style=flat-square" alt="DAX">
  <img src="https://img.shields.io/badge/Pages-8-20E2D7?style=flat-square" alt="8 report pages">
  <img src="https://img.shields.io/badge/Status-Complete-2ea44f?style=flat-square" alt="Status: Complete">
</p>

## Overview

This repository contains a complete Power BI business intelligence project built around **AdventureWorks Cycles**, a fictional global manufacturer of bikes, components, clothing, and accessories. It follows the full BI workflow end to end — cleaning raw exports in Power Query, building a star-schema data model, writing DAX measures, designing an 8-page interactive report, and layering in Power BI's AI visuals (Q&A, Decomposition Tree, Key Influencers).

## Key Metrics

| Metric | Value |
|---|---|
| Total Revenue | **$24.9M** |
| Total Profit | **$10.5M** (42.0% margin) |
| Distinct Orders | **25,164** |
| Units Sold | **84,174** |
| Return Rate | **2.17%** |
| Customers | **17,416 active customers** |
| Markets | **6 countries · 3 continents** |
| Date Range | **Jan 2020 – Jun 2022** |

## Key Insights

- **Bikes drive almost all revenue:** Bikes generated about 95% of total revenue while accessories contributed much higher unit volume at lower price points.
- **Australia is a major market:** Australia generated revenue close to the combined United States market despite being a single territory.
- **2022 growth accelerated:** H1 2022 revenue was already close to the full-year 2021 level.
- **Strong customer activation:** The large majority of profiled customers placed at least one order.

## Repository Structure

```text
AdventureWorks-BikeShop/
├── README.md
├── AdventureWorks Report_FINAL.pbix
├── AdventureWorks Raw Data/
├── AdventureWorks Images/
└── AdventureWorks Screenshots/
```

## Dashboard Screenshots

### Executive Dashboard
![Executive Dashboard](AdventureWorks%20Screenshots/AdventureWorks-ExecDashboard.png)

### Regional Map
![Regional Map](AdventureWorks%20Screenshots/AdventureWorks-MapDashboard.png)

### Product Detail
![Product Detail](AdventureWorks%20Screenshots/AdventureWorks-ProductDetailDashboard.png)

### Customer Detail
![Customer Detail](AdventureWorks%20Screenshots/AdventureWorks-CustomerDetailDashboard.png)

## Data Model

The project uses a star-schema-style analytical model with sales and returns facts connected to customer, product, calendar and territory dimensions. The Power BI model supports revenue, profitability, customer, product, return and time-intelligence analysis.

## Report Walkthrough

The final report spans **8 pages** and includes an executive dashboard, regional analysis, product analysis, customer analytics, drill-through pages and Power BI AI visuals.

### Executive Dashboard
- Total Revenue, Orders, Profit and Return Rate KPI cards
- Monthly revenue trend
- Category-level order analysis
- Top products and product performance
- Year and continent filtering

### Regional Map
- Geographic view of business performance across countries and territories

### Product Detail
- Revenue, profit and order performance by product
- Product-level trends and return analysis
- What-if price adjustment analysis

### Customer Detail
- Customer growth and segmentation
- Revenue per customer
- Top customer analysis
- Income-level and occupation segmentation

### AI-Powered Analytics
- Q&A natural-language analysis
- Decomposition Tree
- Key Influencers

## Key DAX & Power BI Skills

- Revenue, profit, orders, returns and return-rate measures
- Month-over-month time intelligence
- Target and what-if calculations
- Power Query data cleaning and transformation
- Star-schema data modeling
- DAX measures and calculated fields
- Drill-through, slicers, tooltips and bookmarks
- Decomposition Tree, Key Influencers and Q&A

## Tools Used

**Power BI Desktop · DAX · Power Query · Data Modeling · Excel/CSV · Business Intelligence · Data Visualization**

## Getting Started

1. Clone or download this repository.
2. Open `AdventureWorks Report_FINAL.pbix` in Power BI Desktop.
3. If Power BI requests data-source paths, point the queries to the CSV files inside `AdventureWorks Raw Data/`.
4. Refresh the report and explore the dashboards.

## Project Outcome

Built an end-to-end business intelligence solution for AdventureWorks, analyzing **$24.9M revenue, $10.5M profit, 25K+ orders and 84K+ units** across global markets, with interactive dashboards and analytical drill-down capabilities.
