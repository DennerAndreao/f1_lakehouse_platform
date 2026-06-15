# Databricks notebook source

# COMMAND ----------

# MAGIC %run ./00_config

# COMMAND ----------

# MAGIC %run ./01_utils

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, col, lit

# =========================
# SETUP
# =========================

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {BRONZE_SCHEMA}")

# COMMAND ----------

# =========================
# RACES (FLATTEN BEFORE SPARK)
# =========================

races_url = f"{BASE_URL}/{SEASON}.json"
races_data = fetch_paginated(races_url, "Races")

races_flat = []

for race in races_data:
    races_flat.append({
        "season": race.get("season"),
        "round": int(race.get("round")) if race.get("round") else None,
        "race_name": race.get("raceName"),
        "date": race.get("date"),

        "circuit_id": race.get("Circuit", {}).get("circuitId"),
        "circuit_name": race.get("Circuit", {}).get("circuitName"),
        "locality": race.get("Circuit", {}).get("Location", {}).get("locality"),
        "country": race.get("Circuit", {}).get("Location", {}).get("country")
    })

df_races = spark.createDataFrame(races_flat) \
    .withColumn("source", lit("ergast_api")) \
    .withColumn("ingestion_timestamp", current_timestamp()) \
    .dropDuplicates(["season", "round"])

df_races.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(f"{BRONZE_SCHEMA}.races")

# =========================
# RESULTS (FLATTEN)
# =========================

results_url = f"{BASE_URL}/{SEASON}/results.json"
races_results = fetch_paginated(results_url, "Races")

results_flat = []

for race in races_results:
    season = race.get("season")
    round_ = int(race.get("round")) if race.get("round") else None
    race_name = race.get("raceName")

    for result in race.get("Results", []):
        driver_number = result.get("number")
        results_flat.append({
            "season": season,
            "round": round_,
            "race_name": race_name,
            "circuit_id": race.get("Circuit", {}).get("circuitId"),

            "driver_id": result.get("Driver", {}).get("driverId"),
            "driver_number": int(driver_number) if driver_number else None,

            "constructor_id": result.get("Constructor", {}).get("constructorId"),
            "constructor_name": result.get("Constructor", {}).get("name"),

            "grid": int(result.get("grid")) if result.get("grid") else None,
            "position": int(result.get("position")) if result.get("position") else None,
            "points": float(result.get("points")) if result.get("points") else None,
            "laps": int(result.get("laps")) if result.get("laps") else None,

            "status": result.get("status"),
            "fastest_lap_time": result.get("FastestLap", {}).get("Time", {}).get("time")
        })

df_results = spark.createDataFrame(results_flat) \
    .withColumn("source", lit("ergast_api")) \
    .withColumn("ingestion_timestamp", current_timestamp()) \
    .dropDuplicates(["season", "round", "driver_id"])

df_results.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(f"{BRONZE_SCHEMA}.results")


# =========================
# SPRINT RESULTS
# =========================

sprint_url = f"{BASE_URL}/{SEASON}/sprint.json"
sprint_data = fetch_paginated(sprint_url,"Races")

sprint_flat = []

for race in sprint_data:
    season = race.get("season")
    round_ = int(race.get("round"))
    race_name = race.get("raceName")

    for result in race.get("SprintResults", []):
        driver_number = result.get("number")
        sprint_flat.append({
            "season": season,
            "round": round_,
            "race_name": race_name,
            "circuit_id": race.get("Circuit", {}).get("circuitId"),	

            "driver_id": result.get("Driver", {}).get("driverId"),
            "driver_number": int(driver_number) if driver_number else None,

            "constructor_id": result.get("Constructor",{}).get("constructorId"),
            "constructor_name": result.get("Constructor", {}).get("name"),

            "grid": int(result.get("grid")) if result.get("grid") else None,
            "position": int(result.get("position")) if result.get("position") else None,
            "points": float(result.get("points")) if result.get("points") else None,
            "laps": int(result.get("laps")) if result.get("laps") else None,

            "status": result.get("status"),
            "fastest_lap_time": result.get("FastestLap",{}).get("Time",{}).get("time")
        })

df_sprint = spark.createDataFrame(sprint_flat) \
    .withColumn("source",lit("ergast_api")) \
    .withColumn("ingestion_timestamp",current_timestamp()) \
    .dropDuplicates(["season","round","driver_id"])

df_sprint.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(f"{BRONZE_SCHEMA}.sprint_results")
