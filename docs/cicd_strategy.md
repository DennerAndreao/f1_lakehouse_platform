# CI/CD Strategy

This document describes the planned CI/CD evolution for the F1 Lakehouse Platform.

## Current CI status

The repository currently has a static Terraform CI workflow:

```text
.github/workflows/terraform-ci.yml
```

It runs:

```text
terraform fmt -check
terraform init -backend=false
terraform validate
```

This workflow intentionally does not use cloud credentials. It validates code structure and formatting without touching remote state, AWS, or Databricks.

## Next CI/CD stage

The authenticated Terraform plan workflow is now implemented. The next stage is improving PR feedback and then designing controlled apply.

Planned order:

```text
1. Static CI
   - fmt
   - validate

2. Authenticated plan [implemented]
   - access remote state
   - refresh AWS and Databricks resources
   - generate a Terraform plan
   - publish plan output in the GitHub Actions job summary
   - do not apply

3. PR feedback [implemented]
   - publish plan summary in pull requests
   - update the same bot comment on repeated runs

4. Controlled deployment
   - apply only from main or manual approval
```

## Authentication strategy

### AWS

Use GitHub Actions OIDC to assume an IAM role in AWS.

Rationale:

- avoids storing long-lived AWS access keys in GitHub Secrets
- issues short-lived credentials per workflow run
- can restrict access to this repository, branch, and workflow context

The AWS role should initially support Terraform plan operations for the `dev` environment:

- read remote state from S3
- use S3 lockfile operations
- read managed AWS resources such as S3 bucket configuration and IAM role/policy/profile

Apply permissions can be introduced later as a separate role or as a protected workflow path.

### Databricks

Use a GitHub Actions secret for the current Databricks token in the first authenticated plan iteration.

Planned secret:

```text
DATABRICKS_TOKEN
```

Rationale:

- simple enough for the current individual project phase
- compatible with the existing Databricks provider configuration
- allows Terraform plan to refresh Unity Catalog resources

Future enterprise evolution:

- replace user PAT with a Databricks service principal
- use OAuth machine-to-machine authentication where supported
- restrict CI/CD privileges independently from the human user

## Workflow separation

The project should keep CI/CD staged:

```text
terraform-ci.yml
-> static checks without credentials

terraform-plan.yml
-> authenticated plan, no apply

terraform-apply.yml
-> controlled deployment, later
```

This avoids mixing lightweight validation with privileged deployment behavior.

## Current recommendation

Next recommended step: validate pull request feedback with a small PR, then design a separate controlled `terraform-apply.yml` workflow.

