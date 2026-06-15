# Databricks notebook source

# COMMAND ----------

BASE_URL = "https://api.jolpi.ca/ergast/f1"
SEASON = "2026"

CATALOG = "f1_lakehouse_dev"
SCHEMA = "bronze"
BRONZE_SCHEMA = f"{CATALOG}.{SCHEMA}"
