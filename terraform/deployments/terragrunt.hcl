remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    bucket = local.remote_state_vars.locals.remote_state_bucket

    key     = "${local.common_vars.locals.service}/${local.common_vars.locals.stage}/${basename(path_relative_to_include())}/terraform.tfstate"
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

locals {
  common_vars       = read_terragrunt_config("${get_terragrunt_dir()}/../env.hcl")
  remote_state_vars = read_terragrunt_config("${get_terragrunt_dir()}/../remote_state_env.hcl")
  helper_vars       = read_terragrunt_config("${get_parent_terragrunt_dir()}/helpers_env.hcl")
}
