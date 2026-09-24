import pandas as pd
import numpy as np

from src.data_prep import build_weekly_panel, add_features
from src.train_model import train_and_evaluate
from src.inventory_optimization import build_inventory_recommendations


def synthetic_sales():
    rng = np.random.default_rng(42)
    weeks = pd.date_range("2021-01-04", periods=90, freq="W-MON")
    rows = []
    for product in range(1, 7):
        base = 5 + product
        for week_no, week in enumerate(weeks):
            demand = max(0, int(round(base + 2*np.sin(2*np.pi*week_no/13) + rng.normal(0, 1.2))))
            for _ in range(demand):
                rows.append({
                    "OrderDate": week + pd.Timedelta(days=int(rng.integers(0, 7))),
                    "StockDate": week - pd.Timedelta(days=14),
                    "OrderNumber": f"SO{product}{week_no}",
                    "ProductKey": product,
                    "CustomerKey": 1000 + product,
                    "TerritoryKey": 1,
                    "OrderLineItem": 1,
                    "OrderQuantity": 1,
                })
    return pd.DataFrame(rows)


def synthetic_products():
    return pd.DataFrame({
        "ProductKey": range(1, 7),
        "ProductName": [f"Product {i}" for i in range(1, 7)],
        "ProductCost": [10, 12, 15, 20, 25, 30],
        "ProductPrice": [15, 18, 23, 30, 38, 45],
    })


def test_end_to_end_core_pipeline():
    sales = synthetic_sales()
    products = synthetic_products()
    panel = build_weekly_panel(sales, products, top_n_products=6)
    features = add_features(panel)
    result = train_and_evaluate(features, test_weeks=8)
    inv = build_inventory_recommendations(result.predictions, products)

    assert result.metrics["mae"] >= 0
    assert len(result.predictions) > 0
    assert {"reorder_point", "safety_stock", "recommended_order_qty"}.issubset(inv.columns)
    assert (inv["reorder_point"] >= 0).all()
