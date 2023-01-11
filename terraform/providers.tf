terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      "Service" = var.service,
      "Stage"   = var.stage,
    }
  }
}

provider "aws" {
  # Special provider for certs that need
  # to be deployed in us-east-1 (e.g. CloudFront)
  alias  = "acm"
  region = "us-east-1"
  default_tags {
    tags = {
      "Service" = var.service,
      "Stage"   = var.stage,
    }
  }
}
