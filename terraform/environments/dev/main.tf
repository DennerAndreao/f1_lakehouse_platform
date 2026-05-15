locals {
  lakehouse_schemas = toset([
    "bronze",
    "silver",
    "gold",
  ])
}

resource "databricks_catalog" "lakehouse" {
  name         = var.catalog_name
  comment      = "Development catalog for the F1 Lakehouse platform."
  storage_root = "s3://${var.s3_bucket_name}/dev/managed"
}

resource "databricks_schema" "lakehouse" {
  for_each     = local.lakehouse_schemas
  catalog_name = databricks_catalog.lakehouse.name
  name         = each.value
  comment      = "${title(each.value)} layer schema for the F1 Lakehouse platform."
}
