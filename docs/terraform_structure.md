# Terraform Structure

This document explains the current Terraform layout and the responsibility of each layer.

## Layout

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
```

## bootstrap

Documents infrastructure required before Terraform can safely operate.

Current bootstrap dependency:

```text
S3 bucket: f1-lakehouse-terraform-state
```

This bucket stores the remote state for the `dev` environment.

## environments/dev

The executable root module for the current development environment.

It composes:

- AWS provider
- Databricks provider
- lakehouse storage module
- storage access IAM module
- Unity Catalog foundation module
- Unity Catalog governance module
- Databricks Storage Credential
- Databricks External Location

## modules/catalog_foundation

Creates the Unity Catalog catalog and medallion schemas.

Resources:

- `databricks_catalog`
- `databricks_schema` with `for_each`

## modules/lakehouse_storage

Manages the S3 lakehouse bucket and bucket-level controls.

Resources:

- `aws_s3_bucket`
- `aws_s3_bucket_versioning`
- `aws_s3_bucket_public_access_block`
- `aws_s3_bucket_ownership_controls`
- `aws_s3_bucket_server_side_encryption_configuration`

## modules/storage_access_iam

Manages the AWS IAM layer used by Databricks to access the lakehouse bucket.

Resources:

- `aws_iam_role`
- `aws_iam_role_policy`
- `aws_iam_instance_profile`

## modules/unity_catalog_governance

Manages Unity Catalog grants for the current dev principal.

Resources:

- `databricks_grant` on catalog
- `databricks_grant` on schemas
- `databricks_grant` on external location

## Import strategy

Many resources existed before Terraform. They were adopted through this pattern:

```text
declare resource in code
import existing resource into state
run plan
reconcile drift
apply only intentional changes
```

This avoided recreating working infrastructure and mirrors how real platform migrations often happen.
