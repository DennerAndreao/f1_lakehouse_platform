# Databricks notebook source

# COMMAND ----------

# MAGIC %run ./00_setup

# COMMAND ----------

from pyspark.sql.functions import col

df = spark.table(f"{BRONZE_SCHEMA}.constructors")

df_dim_constructor = df.select(
    col("constructor_id"),
    col("name"),
    col("nationality")
).dropDuplicates(["constructor_id"])

df_dim_constructor.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(f"{SILVER_SCHEMA}.dim_constructor")
