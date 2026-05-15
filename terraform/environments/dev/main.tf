locals {
  lakehouse_schemas = toset([
    "bronze",
    "silver",
    "gold",
  ])
}

resource "databricks_storage_credential" "lakehouse" {
  name    = var.storage_credential_name
  comment = "Storage credential for the F1 Lakehouse S3 bucket."

  aws_iam_role {
    role_arn = var.storage_credential_iam_role_arn
  }
}

resource "databricks_external_location" "lakehouse" {
  name            = var.external_location_name
  url             = "s3://${var.s3_bucket_name}/"
  credential_name = databricks_storage_credential.lakehouse.id
}

module "catalog_foundation" {
  source       = "../../modules/catalog_foundation"
  catalog_name = var.catalog_name
  storage_root = "s3://${var.s3_bucket_name}/dev/managed"
  schemas      = local.lakehouse_schemas
}
