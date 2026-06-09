# Databricks notebook source

# COMMAND ----------

# MAGIC %run ./00_setup

# COMMAND ----------


spark.sql(f"""

CREATE OR REPLACE TABLE {SCHEMA_GOLD}.constructor_performance
LOCATION 's3://f1-medallion-lakehouse/{SCHEMA_GOLD}/constructor_performance'
AS

WITH combined_results AS (

    SELECT
        constructor_id,
        points,
        position
    FROM {SCHEMA_SILVER}.fact_results

    UNION ALL

    SELECT
        constructor_id,
        points,
        position
    FROM {SCHEMA_SILVER}.fact_sprint_results

)

SELECT
    cr.constructor_id,

    dc.name,
    dc.nationality,

    SUM(cr.points) AS total_points,

    COUNT(*) AS total_events,

    ROUND(
        AVG(cr.position),
        2
    ) AS avg_finish_position,

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

LEFT JOIN {SCHEMA_SILVER}.dim_constructor dc
    ON cr.constructor_id = dc.constructor_id

GROUP BY
    cr.constructor_id,
    dc.name,
    dc.nationality

""")
