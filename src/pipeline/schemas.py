"""Spark schema definitions for retail sales ETL."""

from pyspark.sql.types import DoubleType, StringType, StructField, StructType, TimestampType

RAW_SALES_SCHEMA = StructType(
    [
        StructField("event_id", StringType(), nullable=False),
        StructField("store_id", StringType(), nullable=False),
        StructField("product_id", StringType(), nullable=False),
        StructField("event_ts", StringType(), nullable=False),
        StructField("units_sold", DoubleType(), nullable=True),
        StructField("sales_amount", DoubleType(), nullable=True),
        StructField("currency", StringType(), nullable=True),
    ]
)

CURATED_SCHEMA = StructType(
    [
        StructField("store_id", StringType(), nullable=False),
        StructField("product_id", StringType(), nullable=False),
        StructField("event_ts", TimestampType(), nullable=False),
        StructField("units_sold", DoubleType(), nullable=False),
        StructField("sales_amount", DoubleType(), nullable=False),
    ]
)
