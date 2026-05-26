# Terraform

This directory contains the Infrastructure as Code implementation for the F1 Lakehouse Platform.

The current Terraform design is intentionally split into three concepts:

```text
bootstrap      -> prerequisites that let Terraform operate
environments   -> executable environment compositions
modules        -> reusable infrastructure building blocks
```

## Current environment

```text
terraform/environments/dev
```

The `dev` environment composes AWS and Databricks resources into a governed lakehouse platform.

## Remote state

The `dev` environment uses an S3 backend:

```text
bucket: f1-lakehouse-terraform-state
key:    f1-lakehouse-platform/dev/terraform.tfstate
region: us-east-1
lock:   S3 lockfile enabled
```

The backend bucket is documented under `terraform/bootstrap/` because it must exist before the environment can use it.

## Modules

```text
catalog_foundation        -> Unity Catalog catalog + bronze/silver/gold schemas
lakehouse_storage         -> S3 lakehouse bucket and bucket-level controls
storage_access_iam        -> IAM role, inline policy, and instance profile used by Databricks
unity_catalog_governance  -> Unity Catalog grants for the dev principal
```

## Local execution

```powershell
cd C:\f1_lakehouse_platform\terraform\environments\dev
C:\terraform\terraform.exe init
C:\terraform\terraform.exe validate
C:\terraform\terraform.exe plan
```

Required local authentication:

- AWS credentials for the S3 backend and AWS resources
- Databricks token with scopes needed by the active resources, currently Unity Catalog and SCIM-related operations

## Git hygiene

The following must remain local and uncommitted:

- `.terraform/`
- `terraform.tfvars`
- `*.tfstate`
- `*.tfstate.backup`

The provider lockfile `.terraform.lock.hcl` is committed intentionally for reproducibility.
