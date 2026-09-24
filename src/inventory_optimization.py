from __future__ import annotations

from statistics import NormalDist
import numpy as np
import pandas as pd


def build_inventory_recommendations(
    predictions: pd.DataFrame,
    product_lookup: pd.DataFrame | None = None,
    lead_time_weeks: float = 2.0,
    service_level: float = 0.95,
) -> pd.DataFrame:
    """Turn forecast behavior into interpretable reorder-point recommendations."""
    z = NormalDist().inv_cdf(service_level)

    agg = predictions.groupby("ProductKey").agg(
        avg_weekly_forecast=("PredictedDemand", "mean"),
        forecast_std=("PredictedDemand", "std"),
        actual_avg=("Demand", "mean"),
        mae=("AbsoluteError", "mean"),
    ).reset_index()
    agg["forecast_std"] = agg["forecast_std"].fillna(0)

    agg["safety_stock"] = z * agg["forecast_std"] * np.sqrt(lead_time_weeks)
    agg["reorder_point"] = agg["avg_weekly_forecast"] * lead_time_weeks + agg["safety_stock"]
    agg["recommended_order_qty"] = np.maximum(
        np.ceil(agg["avg_weekly_forecast"] * 4 + agg["safety_stock"]), 0
    )

    if product_lookup is not None:
        keep = [c for c in ["ProductKey", "ProductName", "ProductCost", "ProductPrice"] if c in product_lookup.columns]
        agg = agg.merge(product_lookup[keep].drop_duplicates("ProductKey"), on="ProductKey", how="left")
        if "ProductCost" in agg.columns:
            agg["estimated_cycle_stock_cost"] = agg["recommended_order_qty"] * agg["ProductCost"].fillna(0)

    return agg.sort_values("reorder_point", ascending=False).reset_index(drop=True)
