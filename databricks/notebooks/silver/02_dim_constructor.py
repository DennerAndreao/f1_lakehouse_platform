# Databricks notebook source

# COMMAND ----------

# MAGIC %run ./00_setup

# COMMAND ----------

from pyspark.sql.functions import col

df = spark.table(f"{SCHEMA_BRONZE}.constructors")

df_dim_constructor = df.select(
    col("constructor_id"),
    col("name"),
    col("nationality")
).dropDuplicates(["constructor_id"])

spark.sql(f"USE {SCHEMA_SILVER}")

df_dim_constructor.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .option("path", f"s3://f1-medallion-lakehouse/{SCHEMA_SILVER}/dim_constructor") \
    .saveAsTable(f"{SCHEMA_SILVER}.dim_constructor")
