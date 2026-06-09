# Pipeline Deployment Strategy

This document captures the target enterprise deployment flow for Databricks pipeline code, such as notebooks, jobs, dbt models, and new Gold layer tables.

## Key distinction

Terraform should manage platform infrastructure:

```text
catalogs
schemas
external locations
storage credentials
IAM
workflows
clusters
SQL warehouses
permissions
```

Pipeline deployment should manage data product code:

```text
Bronze ingestion code
Silver transformation code
Gold table/model code
Databricks notebooks
Databricks jobs
future dbt models
```

Terraform builds the station. Pipelines run the trains.

## Target flow for a new Gold table

```text
1. Create a feature branch
   example: feature/gold-driver-standings

2. Add or update the data pipeline code
   future location examples:
   - databricks/notebooks/gold/
   - dbt/models/gold/
   - databricks/resources/jobs/

3. Open a pull request
   - run CI
   - run tests
   - run Terraform plan only if infrastructure changed
   - publish PR feedback

4. Deploy to DEV/STG for validation
   - manually deploy Databricks assets
   - run the job or workflow
   - validate the created/updated Gold table

5. Merge to main
   - accepted code becomes the official version

6. Deploy final environment
   - enterprise target: PROD with approval
   - current project target: controlled DEV until STG/PROD environments exist
```

## Current project mapping

The project currently has one real cloud environment: `dev`.

A future enterprise-style environment layout can evolve toward:

```text
dev
-> current real environment

stg
-> future validation environment for realistic deploy testing

prod
-> future protected production environment
```

Until STG and PROD exist, the project should avoid pretending they are real. Instead, the CI/CD design should remain explicit: Terraform deploys platform infrastructure to dev, while future Databricks Asset Bundles or dbt workflows will deploy pipeline code separately.

## Current notebook migration

The Phase 1 notebooks have been migrated into this repository as Databricks source notebooks:

```text
databricks/notebooks/
??? bronze/
??? silver/
??? gold/
```

This first migration intentionally preserves full-refresh behavior. Incremental ingestion is deferred because the Formula 1 dataset is currently small and the priority is to consolidate repository structure, deployment flow, data quality, and observability first.

## Future workflow direction

Planned separation:

```text
terraform-ci.yml
-> static IaC checks

terraform-plan.yml
-> PR infrastructure plan

terraform-apply.yml
-> controlled infrastructure apply for dev

databricks-deploy.yml
-> future deployment of notebooks/jobs/dbt assets
```

This preserves an enterprise boundary between infrastructure deployment and data pipeline deployment.
