# src/pipeline/

Big Data ingestion and transformation components.

## Files

- `schemas.py`: Spark schemas for raw and curated sales structures.
- `spark_etl.py`: Distributed ETL from raw events to ML-ready aggregates.
- `beam_stream.py`: Streaming prototype for Pub/Sub event normalization.

## Data Engineering Intent

- Enforce explicit schema contracts early.
- Centralize cleansing rules for reproducible lineage.
- Aggregate to feature-ready grain (store-product-hour) for downstream ML.

## ETL Example

`python3 -m src.pipeline.spark_etl --input data/raw/sales.json --output data/curated/sales`
