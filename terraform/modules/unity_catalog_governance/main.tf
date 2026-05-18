resource "databricks_grant" "catalog_engineer" {
  catalog    = var.catalog_name
  principal  = var.principal_name
  privileges = ["USE_CATALOG"]
}

resource "databricks_grant" "schema_engineer" {
  for_each = var.schema_ids

  schema     = each.value
  principal  = var.principal_name
  privileges = ["USE_SCHEMA", "CREATE_TABLE", "MODIFY"]
}

resource "databricks_grant" "external_location_engineer" {
  external_location = var.external_location_id
  principal         = var.principal_name
  privileges        = ["CREATE_MANAGED_STORAGE", "READ_FILES", "WRITE_FILES"]
}
