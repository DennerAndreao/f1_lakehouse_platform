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

The authenticated Terraform plan workflow, PR feedback, and controlled dev apply workflow are implemented and validated.

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

4. Controlled deployment [implemented]
   - separate apply IAM role created
   - manual workflow created
   - apply only from main through the dev environment
   - first GitHub Actions apply validation completed
```

## Authentication strategy

### AWS

Use GitHub Actions OIDC to assume an IAM role in AWS.

Rationale:

- avoids storing long-lived AWS access keys in GitHub Secrets
- issues short-lived credentials per workflow run
- can restrict access to this repository, branch, and workflow context

The project uses separate AWS roles for CI/CD stages:

```text
github-actions-terraform-plan-f1-lakehouse
-> pull requests and plan-only workflows

github-actions-terraform-apply-f1-lakehouse
-> controlled manual apply from main
```

The plan role can read remote state, use the S3 lockfile, and inspect managed AWS resources. The apply role adds controlled write permissions required for Terraform state updates and managed infrastructure changes.

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
-> manual controlled deployment for dev
```

This avoids mixing lightweight validation with privileged deployment behavior.

## Databricks pipeline CI/CD status

The Databricks pipeline deployment path has now started and is intentionally separate from Terraform infrastructure deployment.

Implemented workflows:

```text
.github/workflows/databricks-bundle-validate.yml
-> validates Databricks Asset Bundle changes on pull requests and pushes to main

.github/workflows/databricks-bundle-deploy.yml
-> manually deploys Databricks assets to dev through the GitHub dev environment
```

Current boundary:

```text
validate
-> safe PR / main feedback

deploy
-> controlled manual release of notebooks/jobs to dev

run
-> still separate; next optional workflow
```

This mirrors an enterprise pattern where code deployment and pipeline execution are related but not automatically fused.

## Current recommendation

Next recommended step: add a controlled manual Databricks Bundle run workflow for dev. This will allow the deployed `f1_lakehouse_full_refresh` job to be triggered from GitHub Actions without mixing infrastructure deployment, pipeline asset deployment, and data processing in a single workflow.

