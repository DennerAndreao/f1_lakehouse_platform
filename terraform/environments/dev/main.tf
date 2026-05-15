locals {
  bronze_schema = "bronze"
  silver_schema = "silver"
  gold_schema   = "gold"
}

resource "databricks_catalog" "lakehouse" {
  name         = var.catalog_name
  comment      = "Development catalog for the F1 Lakehouse platform."
  storage_root = "s3://${var.s3_bucket_name}/dev/managed"
}
