# Databricks notebook source

# COMMAND ----------

# MAGIC %run ./00_setup

# COMMAND ----------

from pyspark.sql.functions import col, to_date

df = spark.table(f"{BRONZE_SCHEMA}.races")

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

df_dim_race.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(f"{SILVER_SCHEMA}.dim_race")
