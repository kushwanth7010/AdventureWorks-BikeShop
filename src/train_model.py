from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor

from .data_prep import feature_columns


@dataclass
class TrainingResult:
    model: XGBRegressor
    metrics: dict[str, float]
    predictions: pd.DataFrame
    feature_importance: pd.DataFrame


def mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    mask = y_true != 0
    if not np.any(mask):
        return float("nan")
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100)


def train_and_evaluate(df: pd.DataFrame, test_weeks: int = 12, random_state: int = 42) -> TrainingResult:
    max_week = df["Week"].max()
    split_week = max_week - pd.Timedelta(weeks=test_weeks - 1)
    train = df[df["Week"] < split_week].copy()
    test = df[df["Week"] >= split_week].copy()
    if train.empty or test.empty:
        raise ValueError("Insufficient history for temporal train/test split.")

    features = feature_columns(df)
    X_train, y_train = train[features], train["Demand"]
    X_test, y_test = test[features], test["Demand"]

    model = XGBRegressor(
        objective="reg:squarederror",
        n_estimators=450,
        learning_rate=0.035,
        max_depth=5,
        min_child_weight=3,
        subsample=0.85,
        colsample_bytree=0.9,
        reg_alpha=0.05,
        reg_lambda=1.0,
        random_state=random_state,
        n_jobs=4,
    )
    model.fit(X_train, y_train)
    pred = np.clip(model.predict(X_test), 0, None)

    naive = np.clip(test["lag_1"].to_numpy(), 0, None)
    metrics = {
        "mae": float(mean_absolute_error(y_test, pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, pred))),
        "mape_nonzero_pct": mape(y_test.to_numpy(), pred),
        "naive_mae": float(mean_absolute_error(y_test, naive)),
        "mae_improvement_vs_naive_pct": float(
            (mean_absolute_error(y_test, naive) - mean_absolute_error(y_test, pred))
            / max(mean_absolute_error(y_test, naive), 1e-9) * 100
        ),
        "train_rows": int(len(train)),
        "test_rows": int(len(test)),
        "test_start": str(split_week.date()),
        "test_end": str(max_week.date()),
    }

    predictions = test[["Week", "ProductKey", "Demand"]].copy()
    predictions["PredictedDemand"] = pred
    predictions["AbsoluteError"] = np.abs(predictions["Demand"] - predictions["PredictedDemand"])

    importance = pd.DataFrame({
        "Feature": features,
        "Importance": model.feature_importances_,
    }).sort_values("Importance", ascending=False)

    return TrainingResult(model, metrics, predictions, importance)


def save_training_outputs(result: TrainingResult, output_dir: str | Path) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "models").mkdir(exist_ok=True)
    joblib.dump(result.model, output_dir / "models" / "xgboost_demand_model.joblib")
    result.predictions.to_csv(output_dir / "test_predictions.csv", index=False)
    result.feature_importance.to_csv(output_dir / "feature_importance.csv", index=False)
    with open(output_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(result.metrics, f, indent=2)
