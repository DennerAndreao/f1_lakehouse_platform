# Databricks notebook source

# COMMAND ----------

# MAGIC %run ./00_config

# COMMAND ----------

spark.sql(f"CREATE DATABASE IF NOT EXISTS {SCHEMA}")
