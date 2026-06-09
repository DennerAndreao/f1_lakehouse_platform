# Databricks notebook source

# COMMAND ----------

SCHEMA_BRONZE = "bronze"
SCHEMA_SILVER = "silver"

spark.sql(f"CREATE DATABASE IF NOT EXISTS {SCHEMA_SILVER}")
