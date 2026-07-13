# Databricks notebook source

# COMMAND ----------

CATALOG = "f1_lakehouse_dev"

BRONZE_SCHEMA = f"{CATALOG}.bronze"
SILVER_SCHEMA = f"{CATALOG}.silver"
GOLD_SCHEMA = f"{CATALOG}.gold"

# COMMAND ----------

from pyspark.sql.functions import col, count as spark_count

quality_results = []


def record_check(layer, table_name, check_name, status, details):
    quality_results.append({
        "layer": layer,
        "table_name": table_name,
        "check_name": check_name,
        "status": status,
        "details": details,
    })


def fail(message):
    raise Exception(f"Data quality check failed: {message}")


def assert_table_exists(layer, table_name):
    if not spark.catalog.tableExists(table_name):
        record_check(layer, table_name, "table_exists", "FAILED", "Table does not exist")
        fail(f"{table_name} does not exist")

    record_check(layer, table_name, "table_exists", "PASSED", "Table exists")


def assert_min_rows(layer, table_name, min_rows=1):
    row_count = spark.table(table_name).count()

    if row_count < min_rows:
        record_check(layer, table_name, "min_rows", "FAILED", f"Expected >= {min_rows}, found {row_count}")
        fail(f"{table_name} has {row_count} rows; expected at least {min_rows}")

    record_check(layer, table_name, "min_rows", "PASSED", f"Found {row_count} rows")


def assert_not_null(layer, table_name, columns):
    df = spark.table(table_name)

    for column_name in columns:
        null_count = df.filter(col(column_name).isNull()).count()

        if null_count > 0:
            record_check(layer, table_name, f"not_null_{column_name}", "FAILED", f"Found {null_count} null values")
            fail(f"{table_name}.{column_name} has {null_count} null values")

        record_check(layer, table_name, f"not_null_{column_name}", "PASSED", "No null values found")


def assert_unique_key(layer, table_name, key_columns):
    df = spark.table(table_name)

    duplicate_count = (
        df.groupBy(*key_columns)
          .agg(spark_count("*").alias("record_count"))
          .filter(col("record_count") > 1)
          .count()
    )

    key_name = "_".join(key_columns)

    if duplicate_count > 0:
        record_check(layer, table_name, f"unique_key_{key_name}", "FAILED", f"Found {duplicate_count} duplicated key groups")
        fail(f"{table_name} has duplicated records for key {key_columns}")

    record_check(layer, table_name, f"unique_key_{key_name}", "PASSED", "No duplicate key groups found")


def assert_no_negative_values(layer, table_name, column_name):
    negative_count = spark.table(table_name).filter(col(column_name) < 0).count()

    if negative_count > 0:
        record_check(layer, table_name, f"no_negative_{column_name}", "FAILED", f"Found {negative_count} negative values")
        fail(f"{table_name}.{column_name} has negative values")

    record_check(layer, table_name, f"no_negative_{column_name}", "PASSED", "No negative values found")

# COMMAND ----------

bronze_required_tables = {
    f"{BRONZE_SCHEMA}.drivers": ["driver_id"],
    f"{BRONZE_SCHEMA}.constructors": ["constructor_id"],
    f"{BRONZE_SCHEMA}.races": ["season", "round"],
    f"{BRONZE_SCHEMA}.results": ["season", "round", "driver_id", "constructor_id"],
}

for table_name, required_columns in bronze_required_tables.items():
    assert_table_exists("bronze", table_name)
    assert_min_rows("bronze", table_name)
    assert_not_null("bronze", table_name, required_columns)

# Sprint can be empty depending on the current F1 season calendar/status.
bronze_optional_tables = {
    f"{BRONZE_SCHEMA}.sprint_results": ["season", "round", "driver_id", "constructor_id"],
}

for table_name, required_columns in bronze_optional_tables.items():
    assert_table_exists("bronze", table_name)
    assert_not_null("bronze", table_name, required_columns)

# COMMAND ----------

silver_required_tables = {
    f"{SILVER_SCHEMA}.dim_driver": ["driver_id"],
    f"{SILVER_SCHEMA}.dim_constructor": ["constructor_id"],
    f"{SILVER_SCHEMA}.dim_race": ["season", "round"],
    f"{SILVER_SCHEMA}.fact_results": ["season", "round", "driver_id"],
}

for table_name, key_columns in silver_required_tables.items():
    assert_table_exists("silver", table_name)
    assert_min_rows("silver", table_name)
    assert_not_null("silver", table_name, key_columns)
    assert_unique_key("silver", table_name, key_columns)

silver_optional_tables = {
    f"{SILVER_SCHEMA}.fact_sprint_results": ["season", "round", "driver_id"],
}

for table_name, key_columns in silver_optional_tables.items():
    assert_table_exists("silver", table_name)
    assert_not_null("silver", table_name, key_columns)
    assert_unique_key("silver", table_name, key_columns)

assert_no_negative_values("silver", f"{SILVER_SCHEMA}.fact_results", "points")
assert_no_negative_values("silver", f"{SILVER_SCHEMA}.fact_sprint_results", "points")

# COMMAND ----------

gold_tables = {
    f"{GOLD_SCHEMA}.driver_performance": ["driver_id"],
    f"{GOLD_SCHEMA}.constructor_performance": ["constructor_id"],
}

for table_name, required_columns in gold_tables.items():
    assert_table_exists("gold", table_name)
    assert_min_rows("gold", table_name)
    assert_not_null("gold", table_name, required_columns)
    assert_no_negative_values("gold", table_name, "total_points")

# COMMAND ----------

quality_df = spark.createDataFrame(quality_results)

display(quality_df)

print("All basic data quality checks passed successfully.")