variable "environment" {
  description = "Logical deployment environment for this Terraform root module."
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Project identifier used in resource naming and documentation."
  type        = string
  default     = "f1-lakehouse"
}

variable "aws_region" {
  description = "AWS region used by the dev environment."
  type        = string
  default     = "us-east-1"
}

variable "aws_account_id" {
  description = "AWS account ID that owns the dev lakehouse resources."
  type        = string
  default     = "290909957115"
}

variable "databricks_host" {
  description = "Databricks workspace URL used by the provider."
  type        = string
}

variable "catalog_name" {
  description = "Unity Catalog catalog name for the dev lakehouse platform."
  type        = string
  default     = "f1_lakehouse_dev"
}

variable "s3_bucket_name" {
  description = "Existing S3 bucket currently used by the lakehouse storage paths."
  type        = string
  default     = "f1-medallion-lakehouse"
}

variable "storage_access_role_name" {
  description = "IAM role assumed by Databricks to access the lakehouse bucket."
  type        = string
  default     = "databricks-s3-ingest-da803-db_s3_iam"
}

variable "storage_access_policy_name" {
  description = "Inline IAM policy attached to the Databricks storage access role."
  type        = string
  default     = "databricks-s3-ingest-da803-access-data-buckets"
}

variable "storage_access_instance_profile_name" {
  description = "IAM instance profile associated with the Databricks storage access role."
  type        = string
  default     = "databricks-s3-ingest-da803-access-data-buckets"
}

variable "storage_access_external_id" {
  description = "External ID used in the Databricks storage access role trust policy."
  type        = string
  default     = "c33ad460-73b5-4d63-acbe-dd7b78ff4cfa"
}

variable "storage_credential_name" {
  description = "Existing Unity Catalog storage credential used to access the S3 lakehouse bucket."
  type        = string
  default     = "db_s3_credentials_databricks-s3-ingest-da803"
}

variable "external_location_name" {
  description = "Existing Unity Catalog external location for the S3 lakehouse bucket."
  type        = string
  default     = "db_s3_external_databricks-s3-ingest-da803"
}
