output "catalog_name" {
  description = "Name of the managed Unity Catalog catalog."
  value       = databricks_catalog.lakehouse.name
}

output "schema_names" {
  description = "Schemas created inside the catalog."
  value       = sort(tolist(var.schemas))
}

output "schema_ids" {
  description = "Fully qualified schema identifiers created inside the catalog."
  value       = toset([for schema in databricks_schema.lakehouse : schema.id])
}
