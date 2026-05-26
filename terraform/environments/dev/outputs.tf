output "environment" {
  description = "Environment represented by this Terraform root module."
  value       = var.environment
}

output "catalog_name" {
  description = "Catalog managed by this environment."
  value       = module.catalog_foundation.catalog_name
}

output "lakehouse_schemas" {
  description = "Schemas currently used by the lakehouse architecture."
  value       = module.catalog_foundation.schema_names
}

output "s3_bucket_name" {
  description = "Current external storage bucket for the lakehouse."
  value       = var.s3_bucket_name
}

output "github_actions_plan_role_arn" {
  description = "IAM role ARN to be used by GitHub Actions for Terraform plan."
  value       = module.github_actions_iam.role_arn
}
