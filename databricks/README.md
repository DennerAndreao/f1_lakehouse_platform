# Databricks Assets

This directory is the future home for Databricks pipeline code.

## Current status

The notebooks under `databricks/notebooks/` were migrated from the Phase 1 repository as Databricks source notebooks (`.py`). This first migration intentionally preserves the original full-refresh behavior and schema references.

```text
databricks/notebooks/
??? bronze/
??? silver/
??? gold/
```

## Why `.py` notebooks instead of `.ipynb`?

Databricks source notebooks are easier to review in Git because pull requests show clean text diffs. This is better for enterprise-style code review than storing notebook JSON.

## Current processing strategy

The project will continue using full refresh for now because the Formula 1 dataset is small and the 2026 season data volume is limited. Incremental ingestion is intentionally deferred until the platform and pipeline deployment model are more mature.

## Future direction

Planned evolution:

```text
1. Version notebooks in this repository
2. Refactor schemas/catalog references for Unity Catalog
3. Introduce Databricks Asset Bundles
4. Deploy notebooks/jobs through GitHub Actions
5. Add data quality and observability
6. Add incremental processing later
```

Terraform remains responsible for infrastructure. Databricks pipeline deployment will be handled separately.
