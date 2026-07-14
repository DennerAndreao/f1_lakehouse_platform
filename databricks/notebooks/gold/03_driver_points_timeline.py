# Databricks notebook source

# COMMAND ----------

# MAGIC %run ./00_setup

# COMMAND ----------


spark.sql(f"""

CREATE OR REPLACE TABLE {GOLD_SCHEMA}.driver_points_timeline
AS

WITH race_points AS (

    SELECT
        round,
        race_name,
        driver_id,
        SUM(points) AS race_points

    FROM {SILVER_SCHEMA}.fact_results

    GROUP BY
        round,
        race_name,
        driver_id

),

sprint_points AS (

    SELECT
        round,
        race_name,
        driver_id,
        SUM(points) AS sprint_points

    FROM {SILVER_SCHEMA}.fact_sprint_results

    GROUP BY
        round,
        race_name,
        driver_id

),

combined AS (

    SELECT
        COALESCE(r.round, s.round) AS round,
        COALESCE(r.race_name, s.race_name) AS race_name,
        COALESCE(r.driver_id, s.driver_id) AS driver_id,
        COALESCE(r.race_points, 0) AS race_points,
        COALESCE(s.sprint_points, 0) AS sprint_points,
        COALESCE(r.race_points, 0)
        +
        COALESCE(s.sprint_points, 0)
        AS total_points

    FROM race_points r

    FULL OUTER JOIN sprint_points s
        ON r.round = s.round
        AND r.driver_id = s.driver_id

)

SELECT
    c.round,
    c.race_name,
    c.driver_id,
    CONCAT(
        dd.given_name,
        ' ',
        dd.family_name
    ) AS driver_name,
    c.race_points,
    c.sprint_points,
    c.total_points,
    SUM(c.total_points)
        OVER (
            PARTITION BY c.driver_id
            ORDER BY c.round
        ) AS cumulative_points

FROM combined c

LEFT JOIN {SILVER_SCHEMA}.dim_driver dd
    ON c.driver_id = dd.driver_id

ORDER BY
    round,
    cumulative_points DESC

""")