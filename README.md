# F1 Lakehouse Platform

Phase 2 evolution of the original F1 Lakehouse project, focused on turning a functional analytical lakehouse into a production-oriented cloud data platform.

The original Phase 1 repository remains the analytical baseline. This repository contains the platform engineering layer: infrastructure as code, cloud storage governance, Unity Catalog foundations, and the path toward CI/CD, observability, and operational maturity.

## Current status

```text
Phase 2 overall: ~90%
IaC foundation: 100%
CI/CD: 100%
Pipeline deployment: operational and executable in dev
Data Quality and audit: MVP implemented and integrated into the workflow
```

## What this repository demonstrates

- Terraform-based Infrastructure as Code
- Separate platform repository from the analytics pipeline repository
- Remote Terraform state on AWS S3 with lockfile support
- AWS + Databricks multi-provider architecture
- Unity Catalog catalog and medallion schemas
- S3 lakehouse bucket managed through Terraform
- IAM role, inline policy, and instance profile for Databricks storage access
- Databricks Storage Credential and External Location
- Unity Catalog grants for the current development principal
- Reusable Terraform modules
- GitHub Actions OIDC roles for Terraform plan and controlled apply
- Pull request Terraform plan feedback
- Manual controlled Terraform apply for dev
- Phase 1 Databricks notebooks migrated as source notebooks
- Databricks notebooks refactored for Unity Catalog `f1_lakehouse_dev`
- Databricks Asset Bundle full-refresh workflow deployed and executed successfully
- Databricks Bundle validation workflow running in GitHub Actions
- Manual Databricks Bundle deploy workflow running successfully for dev
- Databricks pipeline execution validated locally through Asset Bundles
- Manual Databricks Bundle run workflow validated successfully for controlled dev execution
- Basic Data Quality gate executed successfully as part of the Databricks workflow
- Quality-check and execution metadata persisted in Delta for every pipeline run
- Paginated API ingestion validated with 198 Formula 1 race-result records
- `driver_points_timeline` Gold table deployed and executed through GitHub Actions
- Power BI dashboard consuming Gold tables from `f1_lakehouse_dev`

## Architecture summary

```text
AWS S3 + IAM
    ↓
Databricks Storage Credential
    ↓
Databricks External Location
    ↓
Unity Catalog
    ↓
f1_lakehouse_dev
├── bronze
├── silver
└── gold
```

See [`docs/architecture.md`](docs/architecture.md) for the full architecture overview. See [`docs/cicd_strategy.md`](docs/cicd_strategy.md) for the CI/CD roadmap and authentication strategy. See [`docs/pipeline_deployment_strategy.md`](docs/pipeline_deployment_strategy.md) for the future Databricks pipeline deployment model.

## Repository structure

```text
terraform/
├── bootstrap/
├── environments/
│   └── dev/
└── modules/
    ├── catalog_foundation/
    ├── lakehouse_storage/
    ├── storage_access_iam/
    └── unity_catalog_governance/

docs/
├── architecture.md
├── governance.md
├── terraform_structure.md
└── diagrams/
    └── platform_architecture.md
```

## Terraform environment

The current executable environment is:

```text
terraform/environments/dev
```

Common local commands:

```powershell
cd C:\f1_lakehouse_platform\terraform\environments\dev
C:\terraform\terraform.exe init
C:\terraform\terraform.exe validate
C:\terraform\terraform.exe plan
```

`terraform.tfvars` is intentionally local and ignored by Git.


## Latest implementation checkpoint

The platform now has a working Databricks Asset Bundle deployment loop for the dev environment:

```text
Git source notebooks
-> Databricks Bundle validate
-> Databricks Bundle deploy
-> Databricks Bundle run
-> Bronze/Silver/Gold full refresh
```

The full-refresh Databricks job has run successfully from both the local CLI and GitHub Actions. The GitHub Actions workflows for Bundle validation, controlled Bundle deployment, and controlled Bundle execution have passed. The `quality_basic_checks` task has also run successfully at the end of the workflow.

The Bronze pagination helper now uses the source API total record count, which fixed the nested-results pagination issue. The pipeline now ingests all 198 available 2026 result records. The `driver_points_timeline` Gold table was added, validated through the GitHub Actions deployment flow, and is available to the Power BI dashboard.

The quality gate persists its results and Databricks job metadata in `f1_lakehouse_dev.quality.data_quality_results` before failing the workflow. This provides a lightweight, durable audit trail appropriate for the current personal-project scope.

Next implementation step: parameterize catalog and season by Bundle target before starting incremental ingestion or introducing additional environments.

## Roadmap

### 1. Infrastructure as Code

- [x] Terraform foundation
- [x] Remote S3 backend
- [x] AWS provider
- [x] Databricks provider
- [x] S3 lakehouse storage
- [x] IAM storage access
- [x] Unity Catalog foundation
- [x] Unity Catalog governance grants
- [x] Reusable modules
- [ ] Final documentation polish

### 2. CI/CD

- [x] Terraform formatting check
- [x] Terraform validation workflow
- [x] GitHub Actions authentication strategy for plan
- [x] Authenticated Terraform plan workflow
- [x] Plan output in GitHub Actions summary
- [x] Pull request plan comments
- [x] Separate IAM role for controlled apply
- [x] Controlled deployment workflow
- [x] First manual apply validation from GitHub Actions
- [x] Databricks Bundle validation workflow
- [x] Manual Databricks Bundle deploy workflow for dev
- [x] Optional manual Databricks Bundle run workflow
- [x] First manual Databricks Bundle run validation from GitHub Actions

### 3. Databricks pipeline code

- [x] Bring Phase 1 notebooks into the platform repository
- [x] Store notebooks as Databricks `.py` source notebooks
- [x] Refactor notebooks for Unity Catalog catalog/schema naming
- [x] Prepare Databricks Asset Bundles structure
- [x] Validate Databricks Asset Bundle with Databricks CLI
- [x] Deploy Databricks Asset Bundle to dev
- [x] Execute full-refresh workflow through Databricks Bundle
- [x] Add Databricks Bundle validation workflow in GitHub Actions
- [x] Add Databricks pipeline deployment workflow in GitHub Actions
- [x] Add optional Databricks bundle run workflow in GitHub Actions
- [x] Validate full-refresh execution from GitHub Actions
- [x] Fix nested API pagination for full season result ingestion
- [x] Add `driver_points_timeline` Gold table
- [x] Validate a new Gold table through GitHub Actions deploy and run workflows
- [x] Connect the Power BI dashboard to `f1_lakehouse_dev.gold`
- [ ] Parameterize catalog and season by Bundle target

### 4. Data quality

- [x] Basic Bronze and Silver validation rules
- [x] Required-key, volume, uniqueness, and non-negative-value checks
- [x] Run basic quality checks at the end of the full-refresh workflow
- [x] Validate the `driver_points_timeline` Gold table in the quality gate
- [x] Persist quality results in `f1_lakehouse_dev.quality.data_quality_results`
- [x] Record all check results before failing the job
- [ ] Silver referential checks
- [ ] Warning and failure severity levels
- [ ] Gold business rule checks, including cumulative-points reconciliation
- [x] Persist-and-fail handling for critical validation failures

### 5. Observability

- [x] Lightweight quality and execution audit trail in `data_quality_results`
- [ ] Execution metrics
- [ ] Data quality metrics
- [ ] Operational dashboard

The Data Quality and Observability MVP is complete for the current personal-project scope. A dashboard, alerts, and richer per-task metrics remain intentionally deferred.

### 6. Incremental ingestion

Deferred intentionally while the data volume remains small and data quality plus observability are being consolidated.

- [ ] Watermark strategy
- [ ] Incremental race/season ingestion
- [ ] Delta merge strategy
- [ ] Batch metadata

## Relationship to Phase 1

Phase 1 proved the analytical lakehouse pattern with Formula 1 data and Power BI reporting.

Phase 2 turns that foundation into a governed platform layer, emphasizing reproducibility, cloud-native architecture, security boundaries, and operational readiness.

