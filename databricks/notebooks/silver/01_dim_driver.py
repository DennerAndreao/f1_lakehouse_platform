# Databricks notebook source

# COMMAND ----------

# MAGIC %run ./00_setup

# COMMAND ----------

from pyspark.sql.functions import col

df = spark.table(f"{SCHEMA_BRONZE}.drivers")

df_dim_driver = df.select(
    col("driver_id"),
    col("permanent_number"),
    col("code"),
    col("given_name"),
    col("family_name"),
    col("date_of_birth"),
    col("nationality")
).dropDuplicates(["driver_id"])

spark.sql(f"USE {SCHEMA_SILVER}")

df_dim_driver.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .option("path", f"s3://f1-medallion-lakehouse/{SCHEMA_SILVER}/dim_driver") \
    .saveAsTable(f"{SCHEMA_SILVER}.dim_driver")
