output "role_name" {
  description = "IAM role name used by GitHub Actions for Terraform plan."
  value       = aws_iam_role.terraform_plan.name
}

output "role_arn" {
  description = "IAM role ARN used by GitHub Actions for Terraform plan."
  value       = aws_iam_role.terraform_plan.arn
}
