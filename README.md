# enterprise_data_ai_factory

## Executive Summary

`enterprise_data_ai_factory` is a production-style learning repository for building a real-time retail sales anomaly detection platform. It demonstrates how to ingest streaming sales events, process them at scale, engineer robust ML features, train and serve anomaly models, and monitor behavior in near real-time. The end goal is to detect unusual sales patterns (for example, sudden spikes, drops, or distribution shifts) before they become business incidents.

## Technology Stack

| Technology | Role in this Project | Why we use it |
|---|---|---|
| NumPy | Vectorized feature engineering and matrix operations for time-series transformation. | High-performance array math lets us build custom rolling-window features and transformations faster and more clearly than loop-based code. |
| scikit-learn | Model pipeline for anomaly detection (scaling, dimensionality reduction, inference). | `Pipeline` enforces consistent preprocessing + model flow, reducing training/serving skew and making experiments reproducible. |
| PySpark | Distributed ETL on raw retail sales data (1M+ rows and beyond). | Spark scales horizontally and gives a mature DataFrame API for large-scale cleansing, joins, and aggregation. |
| Airflow | Workflow orchestration for ETL, training, scoring, and monitoring jobs. | DAG-driven scheduling and dependencies provide reliable, observable, repeatable ML data operations. |
| Terraform | Infrastructure as Code for cloud resources and environment parity. | Declarative provisioning keeps infrastructure versioned, reviewable, and reproducible across environments. |
| GCP (Pub/Sub, GCS) | Pub/Sub for real-time event ingestion; GCS for durable data/model artifacts. | Pub/Sub handles high-throughput streams; GCS provides cheap, reliable object storage for raw and curated datasets. |
| Apache Beam | Unified stream/batch processing abstraction for event pipelines. | Beam lets us write portable data pipelines that can run across different execution engines while preserving core business logic. |
| Flask | Lightweight model-serving API for anomaly scoring and health endpoints. | Flask is minimal and fast to iterate, ideal for exposing trained model inference endpoints and operational controls. |
| Elasticsearch | Operational monitoring and searchable anomaly/event telemetry. | Fast indexing and rich query capabilities make anomaly exploration, dashboards, and incident triage practical. |
| Hadoop | Data lake and distributed storage/computation ecosystem foundation. | Hadoop-compatible storage and tooling remain a common backbone in enterprise big data architectures. |

## The Big Picture (Architecture Diagram)

```mermaid
flowchart LR
    A[Retail Sales Event Stream] --> B[Data Ingestion: GCP Pub/Sub]
    B --> C[Processing Layer: Apache Beam / PySpark]
    C --> D[ML Transformation: NumPy]
    D --> E[Training and Inference: scikit-learn]
    E --> F[Serving API: Flask]
    F --> G[Monitoring and Search: Elasticsearch]
```

## Deep Dive: How Responsibilities Are Split

### 1) PySpark = Massive Data Engine

PySpark handles the "massive data" problem where raw sales streams and historical backfills can exceed single-machine memory. In this project, PySpark is responsible for:

- Reading raw sales feeds and historical snapshots.
- Cleaning malformed records and enforcing schema consistency.
- Enriching records with calendar and store metadata.
- Producing structured feature-ready tables for the ML layer.

This separation keeps heavy ETL in distributed compute and avoids burdening model code with data quality logic.

### 2) NumPy = Matrix Math and Feature Crafting

NumPy handles high-performance matrix math that turns cleaned time-series into model-friendly tensors. We use NumPy for:

- Vectorized scaling and normalization primitives.
- Custom feature engineering patterns that are easier and faster in arrays than in row loops.
- Transforming time-series into rolling-window matrices to capture local trends and volatility.

This gives us precise control over how business signals are encoded before model training.

### 3) scikit-learn = Intelligence Layer

scikit-learn provides the model pipeline and anomaly intelligence. We design the pipeline to be explicit, auditable, and production-friendly:

- `StandardScaler` for robust normalization of engineered features.
- `PCA` for dimensionality reduction and noise compression.
- `IsolationForest` for unsupervised anomaly detection.

Using `sklearn.pipeline.Pipeline` ensures training and inference run identical preprocessing and model steps, which is a senior-level practice to prevent data leakage and skew.

## Technical Implementation Details

### NumPy Focus (Vectorization + Rolling Window Engineering)

The feature layer will use NumPy to:

- Build rolling windows from time-series sales vectors.
- Compute vectorized statistics (mean, std, deltas, z-like signals) over each window.
- Produce dense feature matrices efficiently for downstream ML.

### scikit-learn Focus (End-to-End Pipeline)

The anomaly model is designed as a full `Pipeline`:

1. `StandardScaler`
2. `PCA`
3. `IsolationForest`

This guarantees deterministic, reusable transformation + model behavior for both offline training and online scoring.

### PySpark Focus (Distributed ETL for 1M+ Rows)

The ETL stage prepares large raw sales datasets into structured ML inputs by:

- Applying schema validation and null-handling.
- Standardizing types and timestamp fields.
- Aggregating and partitioning data for efficient downstream training.

PySpark is the first compute gate that converts noisy operational data into trustworthy analytical inputs.

## DevOps Footprint

This repository is designed to include:

- A `docker-compose.yml` stack to mock local services for development and integration testing.
- A `terraform/` directory that defines the GCP deployment baseline (Pub/Sub topics/subscriptions, buckets, and supporting resources).

Together, these practices create a reproducible path from local experimentation to cloud deployment.
