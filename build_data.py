"""
build_data.py
-------------
Creates the raw (messy) and cleaned sales datasets for this project, and prints
the headline figures used in docs/insights.md.

Run:  python build_data.py

This is a one-off data builder. The actual dashboard is built by hand in Excel
by following docs/build-guide.md — that workbook is the deliverable that shows
the Excel skills. This script only produces the input data and the numbers to
check the dashboard against.
"""

import csv
import os
import random
from datetime import date, timedelta

random.seed(7)
ROOT = os.path.dirname(os.path.abspath(__file__))

REGIONS = ["North", "South", "East", "West"]
CATEGORIES = ["Electronics", "Apparel", "Home & Kitchen", "Grocery", "Beauty"]
CAT_PRICE = {
    "Electronics": (1500, 45000),
    "Apparel": (400, 4000),
    "Home & Kitchen": (300, 8000),
    "Grocery": (50, 2000),
    "Beauty": (150, 3500),
}

START = date(2024, 1, 1)
N = 600


def messy_date(d):
    """Return the date in one of several inconsistent string formats."""
    fmts = [
        d.strftime("%Y-%m-%d"),
        d.strftime("%d/%m/%Y"),
        d.strftime("%d-%b-%Y"),
        d.strftime("%m/%d/%Y"),
    ]
    return random.choice(fmts)


def build():
    clean_rows = []
    for i in range(1, N + 1):
        d = START + timedelta(days=random.randint(0, 364))
        region = random.choice(REGIONS)
        cat = random.choice(CATEGORIES)
        lo, hi = CAT_PRICE[cat]
        unit_price = round(random.uniform(lo, hi), 0)
        units = random.randint(1, 12)
        revenue = round(unit_price * units, 0)
        clean_rows.append({
            "order_id": f"ORD{i:05d}",
            "order_date": d,
            "region": region,
            "product_category": cat,
            "units": units,
            "unit_price": unit_price,
            "revenue": revenue,
        })

    # ---- CLEANED FILE ----
    with open(os.path.join(ROOT, "data", "cleaned_sales_data.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["order_id", "order_date", "region", "product_category",
                    "units", "unit_price", "revenue"])
        for r in clean_rows:
            w.writerow([r["order_id"], r["order_date"].strftime("%Y-%m-%d"),
                        r["region"], r["product_category"], r["units"],
                        int(r["unit_price"]), int(r["revenue"])])

    # ---- RAW (MESSY) FILE ----
    # Introduce realistic, Excel-fixable problems:
    #   inconsistent date formats, mixed case + stray spaces in region,
    #   currency symbols/commas in numbers, some blank revenue cells,
    #   a few duplicate rows.
    messy = []
    for r in clean_rows:
        region = r["region"]
        if random.random() < 0.15:
            region = random.choice([region.upper(), region.lower(), f"  {region} "])
        unit_price_str = f"₹{int(r['unit_price']):,}" if random.random() < 0.3 else str(int(r["unit_price"]))
        revenue_str = "" if random.random() < 0.12 else str(int(r["revenue"]))  # blanks to recompute
        messy.append([
            r["order_id"],
            messy_date(r["order_date"]),
            region,
            r["product_category"].upper() if random.random() < 0.1 else r["product_category"],
            r["units"],
            unit_price_str,
            revenue_str,
        ])

    # add ~10 duplicate rows
    for _ in range(10):
        messy.append(list(random.choice(messy)))

    random.shuffle(messy)
    with open(os.path.join(ROOT, "data", "raw_sales_data.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["order_id", "order_date", "region", "product_category",
                    "units", "unit_price", "revenue"])
        w.writerows(messy)

    return clean_rows


def insights(rows):
    total = sum(r["revenue"] for r in rows)
    by_region = {}
    by_cat = {}
    by_month = {}
    for r in rows:
        by_region[r["region"]] = by_region.get(r["region"], 0) + r["revenue"]
        by_cat[r["product_category"]] = by_cat.get(r["product_category"], 0) + r["revenue"]
        m = r["order_date"].strftime("%Y-%m")
        by_month[m] = by_month.get(m, 0) + r["revenue"]
    aov = total / len(rows)

    print(f"Orders (clean): {len(rows)}")
    print(f"Total revenue: Rs {total:,}")
    print(f"Average order value: Rs {aov:,.0f}")
    print("Revenue by region:")
    for k, v in sorted(by_region.items(), key=lambda x: -x[1]):
        print(f"  {k:6s} Rs {v:,}")
    print("Revenue by category:")
    for k, v in sorted(by_cat.items(), key=lambda x: -x[1]):
        print(f"  {k:16s} Rs {v:,}")
    best_month = max(by_month, key=by_month.get)
    print(f"Best month: {best_month} (Rs {by_month[best_month]:,})")


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    rows = build()
    insights(rows)
