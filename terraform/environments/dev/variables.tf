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

variable "storage_credential_name" {
  description = "Existing Unity Catalog storage credential used to access the S3 lakehouse bucket."
  type        = string
  default     = "db_s3_credentials_databricks-s3-ingest-da803"
}

variable "storage_credential_iam_role_arn" {
  description = "IAM role ARN backing the existing Unity Catalog storage credential."
  type        = string
  default     = "arn:aws:iam::290909957115:role/databricks-s3-ingest-da803-db_s3_iam"
}

variable "external_location_name" {
  description = "Existing Unity Catalog external location for the S3 lakehouse bucket."
  type        = string
  default     = "db_s3_external_databricks-s3-ingest-da803"
}
