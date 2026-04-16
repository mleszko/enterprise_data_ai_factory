"""PySpark ETL for transforming raw sales into ML-ready data."""

from __future__ import annotations

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from src.pipeline.schemas import RAW_SALES_SCHEMA


def build_spark_session(app_name: str = "retail-sales-etl") -> SparkSession:
    return SparkSession.builder.appName(app_name).master("local[*]").getOrCreate()


def clean_sales_dataframe(raw_df: DataFrame) -> DataFrame:
    """Clean and standardize raw sales records.

    Senior pattern: keep cleansing deterministic and explicit; every business
    rule should be encoded in one place so lineage and auditability are clear.
    """
    cleaned = (
        raw_df.withColumn("event_ts", F.to_timestamp("event_ts"))
        .withColumn("units_sold", F.col("units_sold").cast("double"))
        .withColumn("sales_amount", F.col("sales_amount").cast("double"))
        .dropna(subset=["event_id", "store_id", "product_id", "event_ts"])
        .filter(F.col("units_sold").isNotNull() & (F.col("units_sold") >= 0.0))
        .filter(F.col("sales_amount").isNotNull() & (F.col("sales_amount") >= 0.0))
        .dropDuplicates(["event_id"])
    )
    return cleaned


def create_ml_ready_dataset(clean_df: DataFrame) -> DataFrame:
    """Aggregate into store-product-hour grain for downstream ML."""
    return (
        clean_df.withColumn("event_hour", F.date_trunc("hour", "event_ts"))
        .groupBy("store_id", "product_id", "event_hour")
        .agg(
            F.sum("units_sold").alias("units_sold"),
            F.sum("sales_amount").alias("sales_amount"),
        )
        .withColumnRenamed("event_hour", "event_ts")
        .orderBy("store_id", "product_id", "event_ts")
    )


def run_etl(input_path: str, output_path: str) -> None:
    spark = build_spark_session()
    raw_df = spark.read.schema(RAW_SALES_SCHEMA).json(input_path)
    cleaned = clean_sales_dataframe(raw_df)
    curated = create_ml_ready_dataset(cleaned)
    curated.write.mode("overwrite").parquet(output_path)
    spark.stop()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run Spark ETL for sales")
    parser.add_argument("--input", required=True, help="Raw JSON input path")
    parser.add_argument("--output", required=True, help="Curated parquet output path")
    args = parser.parse_args()

    run_etl(args.input, args.output)
