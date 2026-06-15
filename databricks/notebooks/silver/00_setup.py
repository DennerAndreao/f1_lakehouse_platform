# Databricks notebook source

# COMMAND ----------

CATALOG = "f1_lakehouse_dev"
SCHEMA_BRONZE = "bronze"
SCHEMA_SILVER = "silver"

BRONZE_SCHEMA = f"{CATALOG}.{SCHEMA_BRONZE}"
SILVER_SCHEMA = f"{CATALOG}.{SCHEMA_SILVER}"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {SILVER_SCHEMA}")
