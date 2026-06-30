# F1 Lakehouse Platform

Phase 2 evolution of the original F1 Lakehouse project, focused on turning a functional analytical lakehouse into a production-oriented cloud data platform.

The original Phase 1 repository remains the analytical baseline. This repository contains the platform engineering layer: infrastructure as code, cloud storage governance, Unity Catalog foundations, and the path toward CI/CD, observability, and operational maturity.

## Current status

```text
Phase 2 overall: ~82%
IaC foundation: 100%
CI/CD: ~96%
Pipeline deployment: operational in dev
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

The full-refresh Databricks job has already run successfully from the local CLI, and the GitHub Actions workflows for Bundle validation and controlled Bundle deployment have also passed.

Next controlled CI/CD step: add an optional manual workflow to run the deployed Databricks job from GitHub Actions, keeping deployment and execution as separate operational actions.

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
- [ ] Optional manual Databricks Bundle run workflow

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
- [ ] Add optional Databricks bundle run workflow in GitHub Actions

### 4. Data quality

- [ ] Bronze validation rules
- [ ] Silver referential and deduplication checks
- [ ] Gold business rule checks
- [ ] Failure handling strategy

### 5. Observability

- [ ] Pipeline audit tables
- [ ] Execution metrics
- [ ] Data quality metrics
- [ ] Operational dashboard

### 6. Incremental ingestion

Deferred intentionally while the data volume remains small and the platform/pipeline deployment model is still being consolidated.

- [ ] Watermark strategy
- [ ] Incremental race/season ingestion
- [ ] Delta merge strategy
- [ ] Batch metadata

## Relationship to Phase 1

Phase 1 proved the analytical lakehouse pattern with Formula 1 data and Power BI reporting.

Phase 2 turns that foundation into a governed platform layer, emphasizing reproducibility, cloud-native architecture, security boundaries, and operational readiness.

