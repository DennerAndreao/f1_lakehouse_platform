# Databricks notebook source

# COMMAND ----------

# MAGIC %run ./00_setup

# COMMAND ----------

from pyspark.sql.functions import col

df = spark.table(f"{BRONZE_SCHEMA}.drivers")

df_dim_driver = df.select(
    col("driver_id"),
    col("permanent_number"),
    col("code"),
    col("given_name"),
    col("family_name"),
    col("date_of_birth"),
    col("nationality")
).dropDuplicates(["driver_id"])

df_dim_driver.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(f"{SILVER_SCHEMA}.dim_driver")
