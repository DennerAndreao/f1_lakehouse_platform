# CI/CD Strategy

The repository uses small, explicit workflows appropriate for a personal dev environment.

## Terraform

```text
terraform-ci.yml
-> fmt and validate on pull requests and main

terraform-plan.yml
-> authenticated plan and pull-request comment

terraform-apply.yml
-> manual apply through the GitHub dev environment
```

AWS authentication uses GitHub Actions OIDC. Terraform plan and apply use separate IAM roles. The Databricks provider currently receives `DATABRICKS_TOKEN` from the GitHub `dev` environment.

## Databricks

```text
databricks-bundle-validate.yml
-> validates Bundle changes on pull requests and main

databricks-bundle-deploy.yml
-> manual Bundle deployment to dev

databricks-bundle-run.yml
-> manual execution of the deployed full-refresh job
```

Deployment and execution are intentionally separate: a code change is validated, deployed, then run only when the operator chooses to process data.
