# Terraform Structure

```text
terraform/
├── bootstrap/         remote-state prerequisite notes
├── environments/dev/  executable root module
└── modules/           reusable AWS and Databricks components
```

The dev root composes `lakehouse_storage`, `storage_access_iam`, `catalog_foundation`, `unity_catalog_governance`, and `github_actions_iam`, plus the Databricks Storage Credential and External Location.

See [`terraform/README.md`](../terraform/README.md) for local commands, backend details, and module responsibilities.
