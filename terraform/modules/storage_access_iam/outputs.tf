output "role_name" {
  description = "Name of the Databricks storage access IAM role."
  value       = aws_iam_role.storage_access.name
}

output "role_arn" {
  description = "ARN of the Databricks storage access IAM role."
  value       = aws_iam_role.storage_access.arn
}

output "instance_profile_name" {
  description = "Name of the associated IAM instance profile."
  value       = aws_iam_instance_profile.storage_access.name
}
