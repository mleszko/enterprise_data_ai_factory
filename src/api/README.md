# src/api/

Flask inference service layer.

## Files

- `app.py`: Flask app factory and startup entrypoint.
- `routes.py`: `/health` and `/score` endpoint handlers.

## API Contracts

- `GET /health`
  - Returns service liveness.
- `POST /score`
  - Input: JSON payload with `sales` list.
  - Output: anomaly predictions, anomaly count, and decision scores.

## Run Locally

`python3 -m src.api.app`

Then:

- `curl http://127.0.0.1:5000/health`
- `curl -X POST http://127.0.0.1:5000/score -H 'Content-Type: application/json' --data @data/inference/sales_series.json`
