# Databricks notebook source

# COMMAND ----------

# MAGIC %run ./00_setup

# COMMAND ----------


spark.sql(f"""

CREATE OR REPLACE TABLE {GOLD_SCHEMA}.constructor_performance
AS

WITH combined_results AS (

    SELECT
        constructor_id,
        points,
        position
    FROM {SILVER_SCHEMA}.fact_results

    UNION ALL

    SELECT
        constructor_id,
        points,
        position
    FROM {SILVER_SCHEMA}.fact_sprint_results

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

LEFT JOIN {SILVER_SCHEMA}.dim_constructor dc
    ON cr.constructor_id = dc.constructor_id

GROUP BY
    cr.constructor_id,
    dc.name,
    dc.nationality

""")
