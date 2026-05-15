output "catalog_name" {
  description = "Name of the managed Unity Catalog catalog."
  value       = databricks_catalog.lakehouse.name
}

output "schema_names" {
  description = "Schemas created inside the catalog."
  value       = sort(tolist(var.schemas))
}
