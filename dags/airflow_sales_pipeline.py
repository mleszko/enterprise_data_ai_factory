"""Airflow DAG orchestrating ETL, model training, and inference refresh."""

from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "data-ai-platform",
    "retries": 1,
}

with DAG(
    dag_id="retail_sales_anomaly_pipeline",
    default_args=default_args,
    description="Orchestrate Spark ETL and sklearn anomaly model lifecycle",
    schedule="@hourly",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["retail", "anomaly", "spark", "ml"],
) as dag:
    spark_etl = BashOperator(
        task_id="spark_etl",
        bash_command=(
            "python -m src.pipeline.spark_etl "
            "--input data/raw/sales.json "
            "--output data/curated/sales"
        ),
    )

    train_model = BashOperator(
        task_id="train_model",
        bash_command=(
            "python -m src.ml.train "
            "--input data/training/sales_series.json "
            "--output models/isolation_forest.joblib"
        ),
    )

    refresh_scores = BashOperator(
        task_id="refresh_scores",
        bash_command=(
            "python -m src.ml.infer "
            "--input data/inference/sales_series.json "
            "--model models/isolation_forest.joblib "
            "--output artifacts/latest_scores.json"
        ),
    )

    spark_etl >> train_model >> refresh_scores
