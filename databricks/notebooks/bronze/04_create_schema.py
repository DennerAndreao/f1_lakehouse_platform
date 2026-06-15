# Databricks notebook source

# COMMAND ----------

# MAGIC %run ./00_config

# COMMAND ----------

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {BRONZE_SCHEMA}")
