# Pipeline Deployment Strategy

Terraform manages the platform foundation: AWS storage, IAM, Unity Catalog, Storage Credential, External Location, and GitHub Actions IAM roles.

The Databricks Asset Bundle manages the pipeline assets: source notebooks and the `f1_lakehouse_full_refresh` job.

## Adding a Gold table

```text
1. Create or update a notebook under databricks/notebooks/gold/
2. Add its task and dependencies in databricks/resources/jobs.yml
3. Extend the quality notebook if the new table needs baseline validation
4. Run databricks bundle validate -t dev
5. Open a pull request
6. Merge, deploy the Bundle manually, then run the job manually
7. Verify the Unity Catalog table and its quality-audit records
```

Gold tables are managed Unity Catalog tables. Do not set an explicit S3 `LOCATION` in the notebooks.

The current model is intentionally dev-only and full-refresh. Incremental ingestion is deferred while the dataset remains small.
