# Architecture

The F1 Lakehouse Platform is the Phase 3 evolution of the original analytical lakehouse project.

Its current role is to provide a governed, reproducible platform for a full-refresh F1 pipeline, controlled CI/CD, and lightweight quality auditing.

## High-level flow

```text
AWS S3 bucket
    ↓
AWS IAM role / policy / instance profile
    ↓
Databricks Storage Credential
    ↓
Databricks External Location
    ↓
Unity Catalog catalog
    ↓
Medallion schemas
```

## Current deployed architecture

```text
AWS
├── S3 bucket: f1-medallion-lakehouse
├── IAM role: Databricks storage access role
├── Inline IAM policy: lakehouse bucket access + managed file events permissions
└── Instance profile: associated with storage access role

Databricks
├── Storage Credential
├── External Location
├── Catalog: f1_lakehouse_dev
└── Schemas
    ├── bronze
    ├── silver
    ├── gold
    └── quality
```

## Design principles

### Reproducibility

Infrastructure is declared in Terraform and tracked through remote state. Existing resources were imported instead of recreated, preserving the real environment while bringing it under governance.

### Separation of concerns

The platform repository is separate from the Phase 2 analytics repository. This avoids mixing notebooks and dashboard assets with platform infrastructure.

### Modular infrastructure

Reusable Terraform modules encode meaningful boundaries:

- cloud storage
- IAM access
- Unity Catalog foundation
- Unity Catalog governance
- GitHub Actions IAM roles

### Deliberate dev-only scope

The project has one executable environment, `dev`. This is intentional for a personal portfolio project; the configuration remains explicit about that scope rather than simulating environments that do not exist.

### Honest governance

Because this is currently an individual project, governance grants are assigned to the real development principal rather than pretending a large organization exists.

## Current limitations

- Only `dev` exists today.
- Ingestion is intentionally full refresh while data volume remains small.
- The quality gate persists a lightweight audit trail in `f1_lakehouse_dev.quality.data_quality_results`; dashboards and alerts are out of scope.
