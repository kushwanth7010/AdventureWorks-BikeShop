# AI-Driven Retail Demand Forecasting & Inventory Optimization

An end-to-end data science project built on the AdventureWorks retail sales data already stored in this repository. The project converts transaction history into weekly SKU demand forecasts and actionable inventory recommendations.

## Business Problem
Retail teams need to answer two linked questions: **how much will each SKU sell next, and how much inventory should be held to meet demand without excessive stock?** This project combines forecasting and inventory logic so model output directly supports a business decision.

## What the project demonstrates
- Python data wrangling with Pandas/NumPy
- Advanced SQL with aggregation and window functions
- Time-series feature engineering: lags, rolling statistics, seasonality
- Gradient-boosted forecasting with XGBoost
- Temporal holdout evaluation using MAE, RMSE and non-zero MAPE
- Baseline comparison against a lag-1 naive forecast
- Model interpretability through feature importance and SHAP-ready artifacts
- Inventory decisions using safety stock, service level and reorder point
- Streamlit dashboard for forecast and inventory insights
- Automated validation with Pytest and GitHub Actions

## Repository Structure
```text
AdventureWorks Raw Data/          # Original CSV data already in this repo
src/
  data_prep.py                    # ingestion, weekly panel, feature engineering
  train_model.py                  # XGBoost training + temporal validation
  inventory_optimization.py       # safety stock + reorder recommendations
  run_pipeline.py                 # end-to-end runner
sql/retail_analysis.sql           # SQL business/feature queries
tests/test_pipeline.py            # end-to-end unit test on synthetic fixtures
app.py                            # Streamlit dashboard
requirements.txt
outputs/                          # generated after pipeline execution
```

## Modeling Approach
1. Concatenate yearly AdventureWorks sales CSVs.
2. Aggregate order quantities to product-week demand.
3. Build a complete weekly panel so zero-demand weeks are represented.
4. Create leakage-safe lag features (1, 2, 4, 8, 13 weeks), rolling statistics and calendar seasonality.
5. Train an `XGBRegressor` on historical weeks.
6. Hold out the most recent 12 weeks as a time-based test set.
7. Compare model MAE with a lag-1 naive forecast.
8. Translate predictions into safety stock, reorder point and recommended order quantities.

## Run Locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m src.run_pipeline --data-dir "AdventureWorks Raw Data" --output-dir outputs
streamlit run app.py
```

## Generated Outputs
Running the pipeline creates:
- `outputs/metrics.json`
- `outputs/test_predictions.csv`
- `outputs/feature_importance.csv`
- `outputs/inventory_recommendations.csv`
- `outputs/modeling_dataset.csv`
- `outputs/models/xgboost_demand_model.joblib`

## Evaluation
The project deliberately avoids hard-coded claims. The exact MAE, RMSE, MAPE and improvement-vs-naive values are produced from the repository's data every time the pipeline is run. This makes resume/interview claims reproducible.

## Inventory Logic
For each product:
- **Safety Stock** = service-level Z score × forecast standard deviation × √lead time
- **Reorder Point** = expected lead-time demand + safety stock
- **Recommended Order Quantity** = approximate four-week forecast demand + safety stock

Default assumptions are a 95% service level and a two-week lead time; both can be changed in code.

## Interview Story
**Business problem → SQL/Python data preparation → time-series features → XGBoost → temporal validation → interpretable drivers → inventory recommendation → business action.**

## Data
The project uses the AdventureWorks raw sales and product lookup files already committed in this repository, including yearly sales files for 2020–2022. No external data download is required to reproduce the pipeline.

## Author
Sampathi Kushwanth — NIT Warangal
