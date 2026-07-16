# Terraform Modules

This directory contains the reusable building blocks composed by `terraform/environments/dev`:

- `catalog_foundation`: Unity Catalog catalog and schemas
- `lakehouse_storage`: S3 lakehouse bucket and bucket-level controls
- `storage_access_iam`: Databricks S3 access role and instance profile
- `unity_catalog_governance`: Unity Catalog grants for the dev principal
- `github_actions_iam`: GitHub Actions OIDC roles for Terraform plan and apply
