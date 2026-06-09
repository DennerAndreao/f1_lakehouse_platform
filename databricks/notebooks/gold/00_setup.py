# Databricks notebook source

# COMMAND ----------

SCHEMA_SILVER = "silver"
SCHEMA_GOLD   = "gold"

spark.sql(f"CREATE DATABASE IF NOT EXISTS {SCHEMA_GOLD}")
