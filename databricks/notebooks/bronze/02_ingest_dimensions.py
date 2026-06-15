# Databricks notebook source

# COMMAND ----------

# MAGIC %run ./00_config

# COMMAND ----------

# MAGIC %run ./01_utils

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, col, to_date, lit

# Ensure Unity Catalog schema exists
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {BRONZE_SCHEMA}")

# =========================
# DRIVERS
# =========================

drivers_url = f"{BASE_URL}/drivers.json"
drivers_data = fetch_paginated(drivers_url, "Drivers")

df_drivers = spark.createDataFrame(drivers_data)

df_drivers = df_drivers.select(
    col("driverId").alias("driver_id"),
    col("permanentNumber").alias("permanent_number"),
    col("code"),
    col("givenName").alias("given_name"),
    col("familyName").alias("family_name"),
    col("dateOfBirth").alias("date_of_birth"),
    col("nationality")
) \
.withColumn("date_of_birth", to_date(col("date_of_birth"))) \
.withColumn("source", lit("ergast_api")) \
.withColumn("ingestion_timestamp", current_timestamp()) \
.dropDuplicates(["driver_id"])

df_drivers.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(f"{BRONZE_SCHEMA}.drivers")

# =========================
# CONSTRUCTORS
# =========================

constructors_url = f"{BASE_URL}/constructors.json"
constructors_data = fetch_paginated(constructors_url, "Constructors")

df_constructors = spark.createDataFrame(constructors_data)

df_constructors = df_constructors.select(
    col("constructorId").alias("constructor_id"),
    col("name"),
    col("nationality")
) \
.withColumn("source", lit("ergast_api")) \
.withColumn("ingestion_timestamp", current_timestamp()) \
.dropDuplicates(["constructor_id"])

df_constructors.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(f"{BRONZE_SCHEMA}.constructors")
