locals {
  lakehouse_schemas = toset([
    "bronze",
    "silver",
    "gold",
  ])
}

module "lakehouse_storage" {
  source      = "../../modules/lakehouse_storage"
  bucket_name = var.s3_bucket_name
}

module "storage_access_iam" {
  source                = "../../modules/storage_access_iam"
  role_name             = var.storage_access_role_name
  inline_policy_name    = var.storage_access_policy_name
  instance_profile_name = var.storage_access_instance_profile_name
  account_id            = var.aws_account_id
  lakehouse_bucket_arn  = module.lakehouse_storage.bucket_arn
  external_id           = var.storage_access_external_id
}

resource "databricks_storage_credential" "lakehouse" {
  name    = var.storage_credential_name
  comment = "Storage credential for the F1 Lakehouse S3 bucket."

  aws_iam_role {
    role_arn = module.storage_access_iam.role_arn
  }
}

resource "databricks_external_location" "lakehouse" {
  name            = var.external_location_name
  url             = "s3://${module.lakehouse_storage.bucket_name}/"
  credential_name = databricks_storage_credential.lakehouse.id
}

module "catalog_foundation" {
  source       = "../../modules/catalog_foundation"
  catalog_name = var.catalog_name
  storage_root = "s3://${module.lakehouse_storage.bucket_name}/dev/managed"
  schemas      = local.lakehouse_schemas
}
