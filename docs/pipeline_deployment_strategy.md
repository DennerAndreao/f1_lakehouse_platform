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
|-- bronze/
|-- silver/
`-- gold/
```

This first migration intentionally preserves full-refresh behavior. Incremental ingestion is deferred because the Formula 1 dataset is currently small and the priority is to consolidate repository structure, deployment flow, data quality, and observability first.

## Bundle foundation

The initial bundle scaffold is now represented by:

```text
databricks.yml
databricks/resources/jobs.yml
```

The first modeled resource is the `f1_lakehouse_full_refresh` job. It is intentionally conservative: it uses a serverless job environment instead of depending on classic clusters.

This keeps the project aligned with enterprise deployment practice while remaining compatible with the current Free Edition workspace constraints.

## First successful pipeline execution

The first Databricks Asset Bundle run completed successfully using the deployed `f1_lakehouse_full_refresh` job.

```text
databricks bundle run -t dev f1_lakehouse_full_refresh
-> TERMINATED SUCCESS
```

This validates the current repository-to-Databricks deployment loop:

```text
source notebooks in Git
-> bundle validate
-> bundle deploy
-> bundle run
-> Bronze/Silver/Gold full refresh
```

## GitHub Actions bundle validation

The repository includes a dedicated workflow for Databricks Bundle validation:

```text
.github/workflows/databricks-bundle-validate.yml
```

It runs on pull requests and pushes to `main` when Databricks assets change:

```text
databricks.yml
databricks/**
```

The workflow performs validation only:

```text
databricks bundle validate -t dev
```

It does not deploy or run jobs. Deployment and execution remain controlled local/manual steps until a separate Databricks deployment workflow is introduced.

## GitHub Actions bundle deployment

The repository includes a manual workflow for controlled Databricks Bundle deployment:

```text
.github/workflows/databricks-bundle-deploy.yml
```

It is triggered manually and targets the GitHub `dev` environment:

```text
workflow_dispatch
-> environment: dev
```

The workflow validates before deploying:

```text
databricks bundle validate -t dev
databricks bundle deploy -t dev
```

It does not run the full-refresh job automatically. Execution remains a separate step so deployment and data processing stay operationally distinct.

The workflow has been validated successfully in GitHub Actions.

## Current operational model

The current Databricks delivery model is now:

```text
Pull Request
-> databricks-bundle-validate.yml
-> validates Bundle structure and resources

Manual dev deploy
-> databricks-bundle-deploy.yml
-> validates and deploys notebooks/jobs to dev

Manual execution
-> currently local CLI
-> future GitHub Actions workflow
```

This is deliberately close to enterprise practice: validation is automatic, deployment is controlled, and execution is explicit.

## Future workflow direction

Planned separation:

```text
terraform-ci.yml
-> static IaC checks

terraform-plan.yml
-> PR infrastructure plan

terraform-apply.yml
-> controlled infrastructure apply for dev

databricks-bundle-validate.yml
-> pull request validation for bundle syntax/resources

databricks-bundle-deploy.yml
-> controlled deployment of notebooks/jobs/dbt assets

databricks-bundle-run.yml
-> next optional controlled execution of deployed jobs
```

This preserves an enterprise boundary between infrastructure deployment and data pipeline deployment.
