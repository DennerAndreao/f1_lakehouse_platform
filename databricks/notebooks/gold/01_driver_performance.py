# Databricks notebook source

# COMMAND ----------

# MAGIC %run ./00_setup

# COMMAND ----------

spark.sql(f"""

CREATE OR REPLACE TABLE {GOLD_SCHEMA}.driver_performance
AS

WITH combined_results AS (

    SELECT
        driver_id,
        points,
        position,
        grid
    FROM {SILVER_SCHEMA}.fact_results

    UNION ALL

    SELECT
        driver_id,
        points,
        position,
        grid
    FROM {SILVER_SCHEMA}.fact_sprint_results

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

LEFT JOIN {SILVER_SCHEMA}.dim_driver dd
    ON cr.driver_id = dd.driver_id

GROUP BY
    cr.driver_id,
    dd.given_name,
    dd.family_name,
    dd.nationality

""")
