output "environment" {
  description = "Environment represented by this Terraform root module."
  value       = var.environment
}

output "lakehouse_schemas" {
  description = "Schemas currently used by the lakehouse architecture."
  value       = sort(tolist(local.lakehouse_schemas))
}

output "s3_bucket_name" {
  description = "Current external storage bucket for the lakehouse."
  value       = var.s3_bucket_name
}
