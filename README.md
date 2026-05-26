# F1 Lakehouse Platform

Phase 2 evolution of the original F1 Lakehouse project, focused on turning a functional analytical lakehouse into a production-oriented cloud data platform.

The original Phase 1 repository remains the analytical baseline. This repository contains the platform engineering layer: infrastructure as code, cloud storage governance, Unity Catalog foundations, and the path toward CI/CD, observability, and operational maturity.

## Current status

```text
Phase 2 overall: ~50%
IaC foundation: ~95%
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

See [`docs/architecture.md`](docs/architecture.md) for the full architecture overview.

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

- [ ] Terraform formatting check
- [ ] Terraform validation workflow
- [ ] Pull request checks
- [ ] GitHub Actions authentication strategy
- [ ] Controlled deployment workflow

### 3. Incremental ingestion

- [ ] Watermark strategy
- [ ] Incremental race/season ingestion
- [ ] Delta merge strategy
- [ ] Batch metadata

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

## Relationship to Phase 1

Phase 1 proved the analytical lakehouse pattern with Formula 1 data and Power BI reporting.

Phase 2 turns that foundation into a governed platform layer, emphasizing reproducibility, cloud-native architecture, security boundaries, and operational readiness.
