resource "databricks_catalog" "lakehouse" {
  name         = var.catalog_name
  comment      = "Development catalog for the F1 Lakehouse platform."
  storage_root = var.storage_root
}

resource "databricks_schema" "lakehouse" {
  for_each     = var.schemas
  catalog_name = databricks_catalog.lakehouse.name
  name         = each.value
  comment      = "${title(each.value)} layer schema for the F1 Lakehouse platform."
}
