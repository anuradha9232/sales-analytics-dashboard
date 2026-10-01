# Data Cleaning Steps

The raw file (`data/raw_sales_data.csv`) is deliberately messy, the way real exported data usually is. This documents every problem in it and exactly how I cleaned it in Excel to produce `data/cleaned_sales_data.csv`. Careful, documented cleaning is the foundation of any reliable analysis - if the data is wrong, every chart built on it is wrong too.

## Problems found in the raw data

| # | Problem | Example | Why it breaks analysis |
|---|---|---|---|
| 1 | Inconsistent date formats | `2024-03-05`, `05/03/2024`, `05-Mar-2024`, `03/05/2024` | Excel can't sort or group by month if dates are text in mixed formats |
| 2 | Currency symbols and commas in numbers | `Rs 12,500` in the unit price column | Cell is treated as text, so SUM ignores it |
| 3 | Inconsistent region text | `North`, `NORTH`, `north`, `  North ` (leading/trailing spaces) | A pivot table counts these as four different regions |
| 4 | Inconsistent category casing | `Electronics` vs `ELECTRONICS` | Same problem - splits one category into two |
| 5 | Blank revenue cells | ~12% of rows have an empty revenue | Missing values understate every total |
| 6 | Duplicate rows | ~10 fully duplicated orders | Double-counts revenue |

## How each was fixed

**1 - Standardise dates**
- Used Text-to-Columns / `DATEVALUE` to convert the text dates into real Excel date values, then applied a single `YYYY-MM-DD` format. Rows where the day/month order was ambiguous (`03/05/2024`) were checked against the order_id sequence to confirm the intended date.

**2 - Strip currency formatting from numbers**
- `=VALUE(SUBSTITUTE(SUBSTITUTE(A2,"Rs ",""),",",""))` to remove the symbol and thousands separators, then confirmed the column sums correctly (a quick `SUM` sanity check - text cells would be skipped).

**3 & 4 - Standardise text**
- `=PROPER(TRIM(A2))` to trim stray spaces and normalise casing, so `  NORTH ` and `north` both become `North`. Verified with a pivot: the region field should show exactly four values, the category field exactly five.

**5 - Recompute blank revenue**
- Revenue is always `units x unit_price`, so blank cells were refilled with `=units*unit_price` rather than guessed or dropped. Kept the rows - dropping them would have lost real orders.

**6 - Remove duplicates**
- Used Data -> Remove Duplicates on `order_id`, since each order ID should appear once. Confirmed the row count dropped back to 600 unique orders.

## Validation after cleaning

Before building anything, I checked the cleaned data holds together:

- Row count = **600** unique orders (duplicates removed).
- Region field = exactly **4** values (North, South, East, West).
- Category field = exactly **5** values.
- No blank revenue cells; every revenue = units x unit_price.
- Total revenue = **Rs 2,24,70,216** - the control figure every dashboard total must match.

That last number is the single most useful check: if a pivot total doesn't equal it, something in the cleaning or the pivot is wrong.
