# F1 Lakehouse Terraform

This directory contains the Infrastructure as Code foundation for Phase 2 of the F1 Lakehouse project.

## Current scope

The first Terraform iteration is intentionally small:

- one executable environment: `dev`
- Databricks provider configuration
- input variables for the current lakehouse context
- no managed resources yet

The goal of this first step is to establish a clean, reproducible Terraform structure before introducing real infrastructure resources.

## Structure

```text
terraform/
├── environments/
│   └── dev/
│       ├── main.tf
│       ├── outputs.tf
│       ├── providers.tf
│       ├── terraform.tfvars.example
│       ├── variables.tf
│       └── versions.tf
└── modules/
    └── README.md
```

## Next evolution

After the foundation is validated, the next step is to add the first real reusable module, likely for Unity Catalog schemas or external storage integration, based on the infrastructure that already exists in the project.
