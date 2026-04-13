terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }

    datadog = {
      source  = "DataDog/datadog"
      version = "~> 3.0"
    }

  }
}

provider "aws" {
  region = "us-east-1"

  default_tags {
    tags = {
      "env"        = "producao"
      "tenant"     = "EnsaiosLocais"
      "managed_by" = "terraform"
      "project"    = "chatbot-core-saas"
    }
  }
}

provider "datadog" {
  api_key = var.datadog_api_key
  app_key = var.datadog_app_key
  api_url = "https://api.datadoghq.com" # Confirme na sua conta se é .com ou .eu
}