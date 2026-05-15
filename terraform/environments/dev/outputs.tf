output "environment" {
  description = "Environment represented by this Terraform root module."
  value       = var.environment
}

output "lakehouse_schemas" {
  description = "Schemas currently used by the lakehouse architecture."
  value = [
    local.bronze_schema,
    local.silver_schema,
    local.gold_schema,
  ]
}

output "s3_bucket_name" {
  description = "Current external storage bucket for the lakehouse."
  value       = var.s3_bucket_name
}
