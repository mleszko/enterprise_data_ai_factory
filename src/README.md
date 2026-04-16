# src/

This directory contains all application source code for the `enterprise_data_ai_factory` project.

## Subpackages

- `ml/`: NumPy + scikit-learn anomaly modeling pipeline.
- `pipeline/`: Big Data ingestion and transformation components (PySpark and Beam).
- `api/`: Flask service exposing model health and scoring endpoints.

## Design Principle

We keep domain responsibilities separated by runtime concern:

1. Data shaping at scale (`pipeline/`)
2. ML representation + intelligence (`ml/`)
3. Online serving (`api/`)

This improves maintainability, testability, and operational debugging.
