# Terraform Bootstrap

This directory documents the infrastructure that must exist before the rest of the Terraform platform can operate safely.

## Current bootstrap dependency

The `dev` environment uses an S3 remote backend for Terraform state:

- Bucket: `f1-lakehouse-terraform-state`
- Region: `us-east-1`
- State key: `f1-lakehouse-platform/dev/terraform.tfstate`
- Locking: S3 lockfile enabled
- Versioning: enabled on the bucket

## Why this is separate

The backend bucket must exist before Terraform can use it to store state. For that reason, it was created as bootstrap infrastructure before the environment configuration was migrated from local state to remote state.

This separation keeps the architecture explicit:

- `bootstrap/` contains prerequisites that let Terraform operate
- `environments/` contains deployable environment composition
- `modules/` contains reusable infrastructure building blocks

## Future evolution

If the project later requires fully automated account bootstrap, this layer can be managed by a separate Terraform root module or a dedicated provisioning process that does not depend on the state backend it creates.
