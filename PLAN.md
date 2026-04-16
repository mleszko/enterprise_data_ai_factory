# PLAN.md

## Purpose of This Plan

This plan defines how we will implement the repository in three execution phases while preserving an enterprise-grade engineering workflow:

- Phase 1: Core ML logic (`NumPy` + `scikit-learn`)
- Phase 2: Big Data pipelines (`PySpark` + streaming foundations)
- Phase 3: API and infrastructure (`Flask` + `docker-compose` + `terraform`)

The intent is to teach both implementation mechanics and senior-level design discipline: reproducibility, observability, separation of concerns, and production-ready interfaces.

---

## Phase 1 — Core ML Logic (NumPy + scikit-learn)

### Goals

- Build feature engineering utilities for time-series sales using NumPy.
- Create a robust anomaly detection pipeline with scikit-learn.
- Package training and inference so the exact same transformation flow is used in both paths.

### Deliverables

- `src/ml/features_numpy.py`
- `src/ml/pipeline.py`
- `src/ml/train.py`
- `src/ml/infer.py`
- `tests/test_features_numpy.py`
- `tests/test_pipeline.py`

### Implementation Strategy

1. **Vectorized feature engineering with NumPy**
   - Convert sorted sales series into rolling-window matrices (no Python row loops for core math paths).
   - Compute window-based statistics (mean, std, min/max spread, trend deltas).
   - Keep feature generation deterministic and stateless for easier reproducibility.

2. **Build full sklearn `Pipeline`**
   - `StandardScaler` -> `PCA` -> `IsolationForest`.
   - Centralize all model hyperparameters in a config object/module.
   - Persist and reload trained artifacts with strict version metadata.

3. **Training and inference contracts**
   - Define clear input/output schemas.
   - Ensure `train.py` and `infer.py` share the same pipeline object factory.
   - Output anomaly scores and thresholded labels in a predictable response format.

### Senior Engineering Standards (Educational Code Commenting)

When we implement Phase 1 code, comments will explicitly teach:

- Why vectorized operations outperform loops in cache behavior and interpreter overhead.
- Why feature matrices should be immutable once produced for model reproducibility.
- Why a single sklearn `Pipeline` object prevents preprocessing skew between fit and predict.
- Why PCA placement before IsolationForest can improve noise handling for high-dimensional windows.

Comments will focus on **tradeoffs and design intent**, not trivial line-by-line narration.

### Validation Plan

- Unit tests for rolling-window correctness and edge cases (short series, NaNs, flat signals).
- Pipeline tests for fit/predict stability and output shape guarantees.
- Smoke run on synthetic retail data with known injected anomalies.

---

## Phase 2 — Big Data Pipelines (PySpark + Streaming Foundations)

### Goals

- Build distributed ETL for 1M+ raw sales rows into ML-ready structured datasets.
- Introduce streaming-compatible ingestion and transformation patterns.
- Produce curated outputs consumable by Phase 1 training/inference code.

### Deliverables

- `src/pipeline/spark_etl.py`
- `src/pipeline/schemas.py`
- `src/pipeline/beam_stream.py` (or equivalent streaming prototype)
- `dags/airflow_sales_pipeline.py`
- `tests/test_spark_etl.py`

### Implementation Strategy

1. **Schema-first ingestion**
   - Define explicit Spark schemas for raw events.
   - Enforce timestamp parsing, numeric casting, and malformed-record routing.

2. **Distributed cleansing and enrichment**
   - Deduplicate events by business keys.
   - Handle nulls and impossible values with consistent business rules.
   - Enrich with dimensions (store, region, promo calendar) where applicable.

3. **Curated ML dataset generation**
   - Aggregate to feature-ready time granularity (for example: store-product-hour).
   - Partition outputs for efficient downstream reads.
   - Emit quality metrics (row counts, null ratios, late-event counts).

4. **Orchestration**
   - Use Airflow DAG steps to separate ingest, clean, feature-curate, and model-train triggers.
   - Ensure each task is idempotent and retry-safe.

### Validation Plan

- Local Spark integration tests on representative sample data.
- Data quality assertions (schema conformance, non-null critical keys, bounded value ranges).
- Performance smoke test validating ETL flow on high-volume synthetic data.

---

## Phase 3 — API and Infrastructure (Flask + Docker + Terraform)

### Goals

- Expose real-time anomaly scoring through a Flask API.
- Provide local environment parity via Docker Compose.
- Define cloud baseline on GCP via Terraform.

### Deliverables

- `src/api/app.py`
- `src/api/routes.py`
- `docker-compose.yml`
- `terraform/` (modules for Pub/Sub, GCS, and supporting resources)
- `infra/README.md`

### Implementation Strategy

1. **Flask inference service**
   - `/health` for service readiness.
   - `/score` for anomaly predictions on incoming sales payloads.
   - Structured JSON responses with traceable score metadata.

2. **Local stack with Docker Compose**
   - Mock dependencies required for local end-to-end iteration.
   - Define service contracts so developers can run a full integration loop on one command.

3. **Terraform for GCP**
   - Provision Pub/Sub topics and subscriptions for ingestion.
   - Provision GCS buckets for raw, curated, and model artifacts.
   - Parameterize environment names and labels for dev/stage/prod parity.

### Validation Plan

- API contract tests for `/health` and `/score`.
- Local end-to-end run: simulated event -> ETL transform -> model score -> monitoring sink.
- Terraform plan validation in CI with environment-specific variable sets.

---

## Cross-Phase Quality Controls

- **Versioned contracts:** all schema and model interfaces are explicitly versioned.
- **Observability-first:** logs, metrics, and failure reasons are emitted at each boundary.
- **Reproducibility:** deterministic seeds and pinned configs for training experiments.
- **Test pyramid discipline:** targeted unit/integration/system tests per component boundary.
- **Documentation as code:** each phase updates README and implementation notes with rationale.

---

## Approval Gate

After your approval of this plan, implementation will begin in order:

1. Phase 1 (ML core)
2. Phase 2 (Big Data pipelines)
3. Phase 3 (API/Infra)

At each phase completion, we will provide runnable verification evidence and concise architectural retrospectives.
