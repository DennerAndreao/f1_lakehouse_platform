# Databricks notebook source

# COMMAND ----------

# MAGIC %run ./00_setup

# COMMAND ----------

from pyspark.sql.functions import col

df = spark.table(f"{SCHEMA_BRONZE}.sprint_results")

df_fact = df.select(
    col("season"),
    col("round"),
    col("race_name"),
    col("circuit_id"),
    col("driver_id"),
    col("driver_number"),
    col("constructor_id"),
    col("constructor_name"),
    col("grid"),
    col("position"),
    col("points"),
    col("laps"),
    col("status"),
    col("fastest_lap_time")
).dropDuplicates(["season", "round", "driver_id"])

spark.sql(f"USE {SCHEMA_SILVER}")

df_fact.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .option("path", f"s3://f1-medallion-lakehouse/{SCHEMA_SILVER}/fact_sprint_results") \
    .saveAsTable(f"{SCHEMA_SILVER}.fact_sprint_results")
