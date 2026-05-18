variable "catalog_name" {
  description = "Unity Catalog catalog managed by the governance module."
  type        = string
}

variable "schema_ids" {
  description = "Schemas that receive engineer grants."
  type        = set(string)
}

variable "external_location_id" {
  description = "External location that receives engineer storage grants."
  type        = string
}

variable "principal_name" {
  description = "Principal that receives the current dev governance grants."
  type        = string
}
