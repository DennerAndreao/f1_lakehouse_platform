# Databricks notebook source

# COMMAND ----------

# MAGIC %run ./00_setup

# COMMAND ----------

from pyspark.sql.functions import col, to_date

df = spark.table(f"{SCHEMA_BRONZE}.races")

df_dim_race = df.select(
    col("season"),
    col("round"),
    col("race_name"),
    to_date(col("date")).alias("race_date"),
    col("circuit_id"),
    col("circuit_name"),
    col("locality"),
    col("country")
).dropDuplicates(["season", "round"])

spark.sql(f"USE {SCHEMA_SILVER}")

df_dim_race.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .option("path", f"s3://f1-medallion-lakehouse/{SCHEMA_SILVER}/dim_race") \
    .saveAsTable(f"{SCHEMA_SILVER}.dim_race")
