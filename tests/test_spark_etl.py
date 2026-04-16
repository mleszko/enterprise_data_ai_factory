from src.pipeline.spark_etl import build_spark_session, clean_sales_dataframe, create_ml_ready_dataset


def test_spark_etl_cleans_and_aggregates_records():
    spark = build_spark_session("test-spark-etl")
    rows = [
        {
            "event_id": "e1",
            "store_id": "s1",
            "product_id": "p1",
            "event_ts": "2025-01-01T10:00:00",
            "units_sold": 2.0,
            "sales_amount": 20.0,
            "currency": "USD",
        },
        {
            "event_id": "e2",
            "store_id": "s1",
            "product_id": "p1",
            "event_ts": "2025-01-01T10:30:00",
            "units_sold": 3.0,
            "sales_amount": 30.0,
            "currency": "USD",
        },
    ]
    df = spark.createDataFrame(rows)

    cleaned = clean_sales_dataframe(df)
    curated = create_ml_ready_dataset(cleaned)

    assert cleaned.count() == 2
    result = curated.collect()
    assert len(result) == 1
    assert result[0]["units_sold"] == 5.0
    assert result[0]["sales_amount"] == 50.0

    spark.stop()
