from __future__ import annotations

import argparse
from pathlib import Path

from .data_prep import load_sales, load_products, build_weekly_panel, add_features
from .train_model import train_and_evaluate, save_training_outputs
from .inventory_optimization import build_inventory_recommendations


def run(data_dir: str, output_dir: str, top_n_products: int = 80, test_weeks: int = 12) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    sales = load_sales(data_dir)
    products = load_products(data_dir)
    panel = build_weekly_panel(sales, products, top_n_products=top_n_products)
    features = add_features(panel)

    features.to_csv(out / "modeling_dataset.csv", index=False)
    result = train_and_evaluate(features, test_weeks=test_weeks)
    save_training_outputs(result, out)

    recommendations = build_inventory_recommendations(result.predictions, products)
    recommendations.to_csv(out / "inventory_recommendations.csv", index=False)

    print("Pipeline completed successfully.")
    for key, value in result.metrics.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retail demand forecasting + inventory optimization pipeline")
    parser.add_argument("--data-dir", default="AdventureWorks Raw Data")
    parser.add_argument("--output-dir", default="outputs")
    parser.add_argument("--top-n-products", type=int, default=80)
    parser.add_argument("--test-weeks", type=int, default=12)
    args = parser.parse_args()
    run(args.data_dir, args.output_dir, args.top_n_products, args.test_weeks)
