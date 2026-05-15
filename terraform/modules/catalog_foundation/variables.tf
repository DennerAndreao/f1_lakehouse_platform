variable "catalog_name" {
  description = "Unity Catalog catalog name for the lakehouse platform."
  type        = string
}

variable "storage_root" {
  description = "Managed storage root for the Unity Catalog catalog."
  type        = string
}

variable "schemas" {
  description = "Schemas that should exist inside the catalog."
  type        = set(string)
}
