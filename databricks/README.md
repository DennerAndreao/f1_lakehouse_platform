# Databricks Assets

This directory is the future home for Databricks pipeline code.

## Current status

The notebooks under `databricks/notebooks/` were migrated from the Phase 1 repository as Databricks source notebooks (`.py`). They now target the Unity Catalog catalog `f1_lakehouse_dev` and use the medallion schemas provisioned by Terraform: `bronze`, `silver`, and `gold`.

```text
databricks/notebooks/
|-- bronze/
|-- silver/
`-- gold/
```

## Why `.py` notebooks instead of `.ipynb`?

Databricks source notebooks are easier to review in Git because pull requests show clean text diffs. This is better for enterprise-style code review than storing notebook JSON.

## Current processing strategy

The project will continue using full refresh for now because the Formula 1 dataset is small and the 2026 season data volume is limited. Incremental ingestion is intentionally deferred until the platform and pipeline deployment model are more mature. Tables are written as Unity Catalog managed tables so storage placement follows the catalog/schema configuration instead of hardcoded table locations.

## Future direction

Planned evolution:

```text
1. Version notebooks in this repository [done]
2. Refactor schemas/catalog references for Unity Catalog [done]
3. Introduce Databricks Asset Bundles
4. Deploy notebooks/jobs through GitHub Actions [done for dev]
5. Add optional controlled GitHub Actions job execution [done]
6. Add data quality and observability
7. Add incremental processing later
```

Terraform remains responsible for infrastructure. Databricks pipeline deployment will be handled separately.


## Databricks Asset Bundle

The repository now includes the first Declarative Automation Bundle / Databricks Asset Bundle scaffold:

```text
databricks.yml
databricks/resources/jobs.yml
```

The first bundle resource is a full-refresh workflow:

```text
f1_lakehouse_full_refresh
```

It models the medallion dependencies explicitly:

```text
Bronze ingestion
-> Silver dimensions/facts
-> Gold analytical tables
```

The job is configured for serverless task execution through a Databricks job environment. This avoids depending on classic clusters, which may not exist in the Free Edition workspace.

Future CI/CD evolution:

```text
databricks bundle validate
-> pull request validation

databricks bundle deploy -t dev
-> manual or controlled dev deployment

databricks bundle run -t dev f1_lakehouse_full_refresh
-> execute the full-refresh job
```


## First successful bundle run

The first full-refresh job execution through Databricks Asset Bundles completed successfully:

```text
databricks bundle run -t dev f1_lakehouse_full_refresh
```

Result:

```text
TERMINATED SUCCESS
```

This confirms that the repository can now deploy and run the Databricks medallion workflow end to end.


## GitHub Actions status

The Databricks Bundle validation and deployment workflows have passed successfully:

```text
databricks-bundle-validate.yml
-> validates bundle configuration and resources

databricks-bundle-deploy.yml
-> manually deploys the bundle to dev

databricks-bundle-run.yml
-> manually runs the deployed full-refresh job
```

The repository includes `databricks-bundle-run.yml`, which successfully triggers the already-deployed `f1_lakehouse_full_refresh` job from GitHub Actions.
