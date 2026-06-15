# Databricks notebook source

# COMMAND ----------

CATALOG = "f1_lakehouse_dev"
SCHEMA_SILVER = "silver"
SCHEMA_GOLD = "gold"

SILVER_SCHEMA = f"{CATALOG}.{SCHEMA_SILVER}"
GOLD_SCHEMA = f"{CATALOG}.{SCHEMA_GOLD}"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {GOLD_SCHEMA}")
