# dags/

Airflow DAG definitions for orchestrating data and model workflows.

## Current DAG

- `airflow_sales_pipeline.py`
  - `spark_etl` -> `train_model` -> `refresh_scores`

## Operational Note

DAG task commands are intentionally plain CLI invocations so they are easy to run manually during debugging.
