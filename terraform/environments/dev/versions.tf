terraform {
  required_version = ">= 1.15.0, < 2.0.0"

  backend "s3" {
    bucket       = "f1-lakehouse-terraform-state"
    key          = "f1-lakehouse-platform/dev/terraform.tfstate"
    region       = "us-east-1"
    use_lockfile = true
  }

  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.115"
    }

    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.45"
    }
  }
}
