# Databricks Assets

This directory contains the pipeline code deployed through the Databricks Asset Bundle defined at the repository root.

## Layout

```text
notebooks/
├── bronze/   API ingestion
├── silver/   normalized dimensions and facts
├── gold/     analytical tables consumed by Power BI
└── quality/  quality checks and lightweight execution audit

resources/jobs.yml  full-refresh job definition
```

The notebooks target the Unity Catalog catalog `f1_lakehouse_dev`. The pipeline intentionally uses full refresh because the F1 dataset is small.

## Delivery flow

```text
Pull request
-> Databricks Bundle Validate

Manual dev deployment
-> Databricks Bundle Deploy

Manual dev execution
-> Databricks Bundle Run
```

The quality task runs after the Gold tasks and appends one record per check to `f1_lakehouse_dev.quality.data_quality_results`.

## Local commands

```powershell
databricks bundle validate -t dev
databricks bundle deploy -t dev
databricks bundle run -t dev f1_lakehouse_full_refresh
```
