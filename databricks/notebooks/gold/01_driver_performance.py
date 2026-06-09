# Databricks notebook source

# COMMAND ----------

# MAGIC %run ./00_setup

# COMMAND ----------

spark.sql(f"""

CREATE OR REPLACE TABLE {SCHEMA_GOLD}.driver_performance
LOCATION 's3://f1-medallion-lakehouse/{SCHEMA_GOLD}/driver_performance'
AS

WITH combined_results AS (

    SELECT
        driver_id,
        points,
        position,
        grid
    FROM {SCHEMA_SILVER}.fact_results

    UNION ALL

    SELECT
        driver_id,
        points,
        position,
        grid
    FROM {SCHEMA_SILVER}.fact_sprint_results

)

SELECT
    cr.driver_id,
    dd.given_name,
    dd.family_name,
    dd.nationality,

    SUM(cr.points) AS total_points,
    COUNT(*) AS total_events,
    ROUND(AVG(cr.position),2) AS avg_finish_position,
    ROUND(AVG(cr.grid),2) AS avg_grid_position,
    SUM(
        CASE
            WHEN cr.position = 1
            THEN 1
            ELSE 0
        END
    ) AS wins,

    SUM(
        CASE
            WHEN cr.position <= 3
            THEN 1
            ELSE 0
        END
    ) AS podiums

FROM combined_results cr

LEFT JOIN {SCHEMA_SILVER}.dim_driver dd
    ON cr.driver_id = dd.driver_id

GROUP BY
    cr.driver_id,
    dd.given_name,
    dd.family_name,
    dd.nationality

""")
