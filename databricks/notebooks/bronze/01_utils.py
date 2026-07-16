# Databricks notebook source

# COMMAND ----------

import requests
import time

def fetch_paginated(endpoint_url, key):
    offset = 0
    limit = 100
    all_data = []

    while True:
        url = f"{endpoint_url}?limit={limit}&offset={offset}"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code}")

        data = response.json()["MRData"]
        total_records = int(data["total"])

        table = [v for k, v in data.items() if k.endswith("Table")][0]
        batch = table.get(key, [])

        all_data.extend(batch)

        offset += limit

        # Some Ergast endpoints paginate nested records (for example,
        # Results inside Races). The number of race objects is therefore not
        # the number of records returned, so use MRData.total for termination.
        if offset >= total_records:
            break

        time.sleep(0.2)

    return all_data
