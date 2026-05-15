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

variable "databricks_host" {
  description = "Databricks workspace URL used by the provider."
  type        = string
}

variable "catalog_name" {
  description = "Unity Catalog catalog name intended for the lakehouse resources."
  type        = string
  default     = "f1_lakehouse"
}

variable "s3_bucket_name" {
  description = "Existing S3 bucket currently used by the lakehouse storage paths."
  type        = string
  default     = "f1-medallion-lakehouse"
}
