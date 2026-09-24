from pathlib import Path
import json
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Retail Demand & Inventory Optimizer", layout="wide")
st.title("AI-Driven Retail Demand Forecasting & Inventory Optimization")
st.caption("AdventureWorks | Python • SQL • XGBoost • Time Series • Explainable ML")

out = Path("outputs")
if not (out / "metrics.json").exists():
    st.warning("Run `python -m src.run_pipeline` first to generate model outputs.")
    st.stop()

metrics = json.loads((out / "metrics.json").read_text())
preds = pd.read_csv(out / "test_predictions.csv", parse_dates=["Week"])
inv = pd.read_csv(out / "inventory_recommendations.csv")
fi = pd.read_csv(out / "feature_importance.csv")

c1, c2, c3, c4 = st.columns(4)
c1.metric("MAE", f"{metrics['mae']:.2f}")
c2.metric("RMSE", f"{metrics['rmse']:.2f}")
c3.metric("MAPE (non-zero)", f"{metrics['mape_nonzero_pct']:.1f}%")
c4.metric("MAE vs Naive", f"{metrics['mae_improvement_vs_naive_pct']:.1f}%")

st.subheader("Forecast vs Actual")
weekly = preds.groupby("Week")[["Demand", "PredictedDemand"]].sum()
st.line_chart(weekly)

st.subheader("Inventory Recommendations")
st.dataframe(inv.head(30), use_container_width=True)

st.subheader("Model Feature Importance")
st.bar_chart(fi.head(15).set_index("Feature"))
