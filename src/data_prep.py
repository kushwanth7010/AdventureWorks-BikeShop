from __future__ import annotations

from pathlib import Path
import glob
import numpy as np
import pandas as pd


def load_sales(data_dir: str | Path) -> pd.DataFrame:
    """Load and concatenate AdventureWorks yearly sales files."""
    data_dir = Path(data_dir)
    files = sorted(glob.glob(str(data_dir / "AdventureWorks Sales Data *.csv")))
    if not files:
        raise FileNotFoundError(
            f"No sales CSVs found in {data_dir}. Expected files named "
            "'AdventureWorks Sales Data YYYY.csv'."
        )
    frames = [pd.read_csv(f, parse_dates=["OrderDate", "StockDate"]) for f in files]
    sales = pd.concat(frames, ignore_index=True)
    required = {"OrderDate", "ProductKey", "OrderQuantity"}
    missing = required - set(sales.columns)
    if missing:
        raise ValueError(f"Missing required sales columns: {sorted(missing)}")
    sales["OrderQuantity"] = pd.to_numeric(sales["OrderQuantity"], errors="coerce").fillna(0)
    sales = sales.dropna(subset=["OrderDate", "ProductKey"])
    sales["ProductKey"] = sales["ProductKey"].astype(int)
    return sales


def load_products(data_dir: str | Path) -> pd.DataFrame:
    path = Path(data_dir) / "AdventureWorks Product Lookup.csv"
    if not path.exists():
        raise FileNotFoundError(f"Missing product lookup: {path}")
    products = pd.read_csv(path)
    keep = [c for c in ["ProductKey", "ProductName", "ProductCost", "ProductPrice"] if c in products.columns]
    products = products[keep].drop_duplicates("ProductKey")
    products["ProductKey"] = products["ProductKey"].astype(int)
    for c in ["ProductCost", "ProductPrice"]:
        if c in products:
            products[c] = pd.to_numeric(products[c], errors="coerce")
    return products


def build_weekly_panel(
    sales: pd.DataFrame,
    products: pd.DataFrame | None = None,
    top_n_products: int = 80,
) -> pd.DataFrame:
    """Create a complete product-week demand panel for the most active SKUs."""
    sales = sales.copy()
    sales["Week"] = sales["OrderDate"].dt.to_period("W-SUN").dt.start_time

    totals = sales.groupby("ProductKey")["OrderQuantity"].sum().sort_values(ascending=False)
    top_products = totals.head(min(top_n_products, len(totals))).index
    sales = sales[sales["ProductKey"].isin(top_products)]

    weekly = (
        sales.groupby(["ProductKey", "Week"], as_index=False)["OrderQuantity"]
        .sum()
        .rename(columns={"OrderQuantity": "Demand"})
    )

    all_weeks = pd.date_range(weekly["Week"].min(), weekly["Week"].max(), freq="W-MON")
    grid = pd.MultiIndex.from_product([top_products, all_weeks], names=["ProductKey", "Week"]).to_frame(index=False)
    panel = grid.merge(weekly, on=["ProductKey", "Week"], how="left")
    panel["Demand"] = panel["Demand"].fillna(0.0)

    if products is not None:
        panel = panel.merge(products, on="ProductKey", how="left")

    return panel.sort_values(["ProductKey", "Week"]).reset_index(drop=True)


def add_features(panel: pd.DataFrame) -> pd.DataFrame:
    """Create leakage-safe lag, rolling and calendar features."""
    df = panel.copy().sort_values(["ProductKey", "Week"])
    grp = df.groupby("ProductKey", group_keys=False)

    for lag in [1, 2, 4, 8, 13]:
        df[f"lag_{lag}"] = grp["Demand"].shift(lag)

    shifted = grp["Demand"].shift(1)
    df["rolling_mean_4"] = shifted.groupby(df["ProductKey"]).transform(lambda s: s.rolling(4).mean())
    df["rolling_std_4"] = shifted.groupby(df["ProductKey"]).transform(lambda s: s.rolling(4).std())
    df["rolling_mean_8"] = shifted.groupby(df["ProductKey"]).transform(lambda s: s.rolling(8).mean())
    df["rolling_mean_13"] = shifted.groupby(df["ProductKey"]).transform(lambda s: s.rolling(13).mean())

    iso = df["Week"].dt.isocalendar()
    df["week_of_year"] = iso.week.astype(int)
    df["month"] = df["Week"].dt.month
    df["quarter"] = df["Week"].dt.quarter
    df["year"] = df["Week"].dt.year
    df["week_sin"] = np.sin(2 * np.pi * df["week_of_year"] / 52.0)
    df["week_cos"] = np.cos(2 * np.pi * df["week_of_year"] / 52.0)

    return df.dropna(subset=["lag_13", "rolling_mean_13"]).reset_index(drop=True)


def feature_columns(df: pd.DataFrame) -> list[str]:
    cols = [
        "ProductKey", "lag_1", "lag_2", "lag_4", "lag_8", "lag_13",
        "rolling_mean_4", "rolling_std_4", "rolling_mean_8", "rolling_mean_13",
        "week_of_year", "month", "quarter", "year", "week_sin", "week_cos",
    ]
    for c in ["ProductCost", "ProductPrice"]:
        if c in df.columns:
            cols.append(c)
    return cols
