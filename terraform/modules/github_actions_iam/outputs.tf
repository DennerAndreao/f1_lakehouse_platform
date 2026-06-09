output "plan_role_name" {
  description = "IAM role name used by GitHub Actions for Terraform plan."
  value       = aws_iam_role.terraform_plan.name
}

output "plan_role_arn" {
  description = "IAM role ARN used by GitHub Actions for Terraform plan."
  value       = aws_iam_role.terraform_plan.arn
}

output "apply_role_name" {
  description = "IAM role name used by GitHub Actions for controlled Terraform apply."
  value       = aws_iam_role.terraform_apply.name
}

output "apply_role_arn" {
  description = "IAM role ARN used by GitHub Actions for controlled Terraform apply."
  value       = aws_iam_role.terraform_apply.arn
}
