# Architecture

The F1 Lakehouse Platform is the Phase 2 evolution of the original analytical lakehouse project.

Its current role is to provide a governed, reproducible platform foundation for future data pipelines, CI/CD, data quality, and observability.

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
    └── gold
```

## Design principles

### Reproducibility

Infrastructure is declared in Terraform and tracked through remote state. Existing resources were imported instead of recreated, preserving the real environment while bringing it under governance.

### Separation of concerns

The platform repository is separate from the Phase 1 analytics repository. This avoids mixing notebooks and dashboard assets with platform infrastructure.

### Modular infrastructure

Reusable Terraform modules encode meaningful boundaries:

- cloud storage
- IAM access
- Unity Catalog foundation
- Unity Catalog governance

### Environment-first design

The current environment is `dev`. Future `prod` support can reuse the same modules with separate backend state and environment-specific inputs.

### Honest governance

Because this is currently an individual project, governance grants are assigned to the real development principal rather than pretending a large organization exists. Future account-level groups can be introduced when the project needs multi-user operation.

## Current limitations

- Only `dev` exists today.
- CI/CD has not yet been implemented.
- Ingestion remains Phase 1-style and has not yet been converted to incremental processing.
- Observability and data quality are planned but not yet implemented.
