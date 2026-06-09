variable "aws_account_id" {
  description = "AWS account ID where the GitHub Actions OIDC role is created."
  type        = string
}

variable "github_owner" {
  description = "GitHub organization or user that owns the repository."
  type        = string
}

variable "github_repository" {
  description = "GitHub repository allowed to assume the Terraform plan role."
  type        = string
}

variable "plan_role_name" {
  description = "IAM role name assumed by GitHub Actions for Terraform plan."
  type        = string
}

variable "apply_role_name" {
  description = "IAM role name assumed by GitHub Actions for controlled Terraform apply."
  type        = string
}

variable "terraform_state_bucket_name" {
  description = "S3 bucket that stores Terraform remote state."
  type        = string
}

variable "terraform_state_key" {
  description = "S3 object key for the dev Terraform state."
  type        = string
}

variable "lakehouse_bucket_name" {
  description = "S3 bucket used by the lakehouse platform."
  type        = string
}

variable "storage_access_role_name" {
  description = "IAM role used by Databricks to access the lakehouse bucket."
  type        = string
}

variable "storage_access_policy_name" {
  description = "Inline IAM policy attached to the Databricks storage access role."
  type        = string
}

variable "storage_access_instance_profile_name" {
  description = "IAM instance profile associated with Databricks storage access."
  type        = string
}
