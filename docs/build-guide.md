# Build Guide: The Excel Dashboard

How the dashboard workbook (`sales_dashboard.xlsx`) is put together from the cleaned data. The control figures to check against are in [`insights.md`](insights.md).

## Sheet layout

| Sheet | Purpose |
|---|---|
| `Data` | The cleaned dataset as an Excel table (`tblSales`) |
| `Dashboard` | KPI cards, summary tables, and the three charts |

## Step 1 - Load and format the data

1. Put `cleaned_sales_data.csv` on the `Data` sheet.
2. Select the range and **Insert -> Table** (Ctrl+T) so it becomes a named table `tblSales`. A table means formulas and charts keep working if rows are added.
3. Add a helper column `Month` = `=TEXT([@order_date],"YYYY-MM")` for the monthly trend.

## Step 2 - Summary tables (on the `Dashboard` sheet)

Build three small summary tables that the charts read from. Each uses `SUMIFS` against `tblSales`:

| Table | Group by | Value |
|---|---|---|
| Revenue by Region | region | `=SUMIFS(tblSales[revenue], tblSales[region], <region>)` |
| Revenue by Category | product_category | `=SUMIFS(tblSales[revenue], tblSales[product_category], <category>)` |
| Monthly Revenue | Month | `=SUMIFS(tblSales[revenue], tblSales[Month], <month>)` |

Sort the Category table from highest revenue to lowest.

## Step 3 - KPI cards (top of the `Dashboard` sheet)

Three summary cells:

- **Total Revenue** = `=SUM(tblSales[revenue])` -> should read **Rs 2,24,70,216**
- **Total Orders** = `=COUNTA(tblSales[order_id])` -> **600**
- **Average Order Value** = Total Revenue / Total Orders -> **Rs 37,450**

Format these as large, bold cells with a label above each - these are the numbers a manager reads first.

## Step 4 - Charts

- **Column chart**: Revenue by Region.
- **Bar chart** (sorted descending): Revenue by Category.
- **Line chart**: Monthly Revenue across 2024.

Each chart reads from its summary table. Give each a clear title and keep it clean (no 3-D, light gridlines).

## Step 5 - Final polish

- Arrange KPI cards across the top, charts below.
- Hide gridlines on the `Dashboard` sheet and use a consistent colour theme.
- Confirm the Total Revenue card equals the control figure before calling it done.

## Level up (optional)

For a more interactive version, the summary tables can be replaced with **PivotTables** and **slicers** (region and category) connected to every chart, so one click filters the whole view at once.
