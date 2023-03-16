remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    bucket = local.remote_state_vars.locals.remote_state_bucket

    key     = "${local.common_vars.locals.service}/${local.common_vars.locals.stage}/${path_relative_to_include()}/terraform.tfstate"
    region  = local.remote_state_vars.locals.remote_state_region
    encrypt = true
    #dynamodb_table = "my-lock-table"
  }
}

generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
  region = "${local.common_vars.locals.aws_region}"
  default_tags {
    tags = {
      "Service" = "${local.common_vars.locals.service}",
      "Stage"   = "${local.common_vars.locals.stage}",
    }
  }
}
EOF
}

inputs = {
  aws_region = local.common_vars.locals.aws_region
  service    = local.common_vars.locals.service
  stage      = local.common_vars.locals.stage
}

locals {
  common_vars       = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  remote_state_vars = read_terragrunt_config(find_in_parent_folders("remote_state_env.hcl"))
  helper_vars = read_terragrunt_config(find_in_parent_folders("helpers_env.hcl"))
}
