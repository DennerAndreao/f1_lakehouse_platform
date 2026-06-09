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
            raise Exception(f"Erro na API: {response.status_code}")

        data = response.json()["MRData"]

        table = [v for k, v in data.items() if k.endswith("Table")][0]
        batch = table.get(key, [])

        if not batch:
            break

        all_data.extend(batch)

        if len(batch) < limit:
            break

        offset += limit
        time.sleep(0.2)

    return all_data
