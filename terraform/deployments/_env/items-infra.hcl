terraform {
  source = "../../../src//blocks/items-infra"

  extra_arguments "common_vars" {
    commands = get_terraform_commands_that_need_vars()
    required_var_files = [
      "${get_terragrunt_dir()}/../_secret_values/items-infra-secret-values.tfvars",
    ]
  }
}

generate "provider_acm" {
  # Special provider for certs that need
  # to be deployed in us-east-1 (e.g. CloudFront)
  path      = "provider_acm.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
  alias  = "acm"
  region = "us-east-1"
  default_tags {
    tags = {
      "Service" = var.service,
      "Stage"   = var.stage,
    }
  }
}
EOF
}

inputs = {
  aws_region                  = local.common_vars.locals.aws_region
  service                     = local.common_vars.locals.service
  stage                       = local.common_vars.locals.stage
  api_gateway_api_mapping_key = "v1"
}

locals {
  common_vars = read_terragrunt_config(find_in_parent_folders("env.hcl"))
}
