variable "role_name" {
  description = "IAM role used by Databricks to access the lakehouse bucket."
  type        = string
}

variable "inline_policy_name" {
  description = "Inline policy attached to the Databricks storage access role."
  type        = string
}

variable "instance_profile_name" {
  description = "Instance profile associated with the Databricks storage access role."
  type        = string
}

variable "account_id" {
  description = "AWS account ID that owns the lakehouse resources."
  type        = string
}

variable "lakehouse_bucket_arn" {
  description = "ARN of the lakehouse S3 bucket."
  type        = string
}

variable "external_id" {
  description = "External ID required by the Databricks Unity Catalog trust relationship."
  type        = string
}
