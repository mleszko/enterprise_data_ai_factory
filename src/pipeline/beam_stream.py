"""Apache Beam streaming prototype for sales ingestion normalization."""

from __future__ import annotations

import json
from typing import Dict, Iterable

import apache_beam as beam


class ParseAndValidateEvent(beam.DoFn):
    """Parse JSON events and emit only valid sales records."""

    def process(self, element: str) -> Iterable[Dict]:
        try:
            payload = json.loads(element)
        except json.JSONDecodeError:
            return

        required = {"event_id", "store_id", "product_id", "event_ts", "sales_amount"}
        if not required.issubset(payload.keys()):
            return

        yield {
            "event_id": str(payload["event_id"]),
            "store_id": str(payload["store_id"]),
            "product_id": str(payload["product_id"]),
            "event_ts": str(payload["event_ts"]),
            "sales_amount": float(payload["sales_amount"]),
            "units_sold": float(payload.get("units_sold", 0.0)),
        }


def build_stream_pipeline(input_topic: str, output_path: str) -> beam.Pipeline:
    """Return a Beam pipeline object for stream parsing and persistence."""
    pipeline = beam.Pipeline()
    (
        pipeline
        | "ReadFromPubSub" >> beam.io.ReadFromPubSub(topic=input_topic)
        | "BytesToString" >> beam.Map(lambda x: x.decode("utf-8"))
        | "ParseAndValidate" >> beam.ParDo(ParseAndValidateEvent())
        | "SerializeJSON" >> beam.Map(json.dumps)
        | "WriteToStorage" >> beam.io.WriteToText(output_path)
    )
    return pipeline
