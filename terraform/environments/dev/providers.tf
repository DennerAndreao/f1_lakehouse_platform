provider "databricks" {
  host = var.databricks_host
}

provider "aws" {
  region = var.aws_region
}
