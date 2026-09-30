# Build Guide: The Excel Dashboard

Step-by-step instructions to build the dashboard workbook (`sales_dashboard.xlsx`) from the cleaned data. Following these produces a one-page interactive dashboard with pivot tables, charts, and slicers.

> The workbook is built by hand in Excel — that's the point of this project, to show the Excel skill. This guide is the recipe; the control figures to check against are in [`insights.md`](insights.md).

## Sheet layout

| Sheet | Purpose |
|---|---|
| `Data` | The cleaned dataset (paste from `cleaned_sales_data.csv`) |
| `Pivots` | The pivot tables that feed the charts |
| `Dashboard` | The final one-page view: KPI cards, charts, slicers |

## Step 1 — Load and format the data

1. Paste `cleaned_sales_data.csv` into the `Data` sheet.
2. Select the range and **Insert → Table** (Ctrl+T) so it becomes a named table `tblSales`. Using a table means pivots auto-expand if rows are added.
3. Add a helper column `Month` = `=TEXT([@order_date],"YYYY-MM")` for the monthly trend.

## Step 2 — Build the pivot tables (on the `Pivots` sheet)

Create four pivots from `tblSales`:

| Pivot | Rows | Values |
|---|---|---|
| Revenue by Region | region | Sum of revenue |
| Revenue by Category | product_category | Sum of revenue |
| Monthly Revenue | Month | Sum of revenue |
| Orders & AOV | region | Count of order_id, Sum of revenue |

For the AOV pivot, add a calculated measure or a cell formula: `AOV = total revenue ÷ order count`.

## Step 3 — KPI cards (top of the `Dashboard` sheet)

Three summary cells, pulling from the pivots or with `SUMPRODUCT`/`GETPIVOTDATA`:

- **Total Revenue** — should read **₹2,24,70,216**
- **Total Orders** — **600**
- **Average Order Value** — **₹37,450**

Format these as large, bold cells with a label above each — these are the numbers a manager reads first.

## Step 4 — Charts

- **Column chart**: Revenue by Region.
- **Bar chart** (sorted descending): Revenue by Category.
- **Line chart**: Monthly Revenue across 2024 (uses the `Month` field).

Give each chart a clear title and remove chart-junk (gridlines light, no 3-D).

## Step 5 — Slicers (interactivity)

Insert slicers for **region** and **product_category**, connect them to all pivots/charts (PivotTable Analyze → Filter Connections). Now clicking "South" filters every card and chart at once — this is what makes it a dashboard rather than a static report.

## Step 6 — Final polish

- Arrange KPI cards across the top, charts below, slicers down one side.
- Freeze the header, hide gridlines on the `Dashboard` sheet, set a consistent colour theme.
- Confirm the Total Revenue card equals the control figure before calling it done.

## Save

Save as `sales_dashboard.xlsx` in the repo root and add a screenshot (`dashboard_screenshot.png`) to the README so the result is visible without opening Excel.
