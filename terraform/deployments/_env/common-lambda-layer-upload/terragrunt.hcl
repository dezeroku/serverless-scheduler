terraform {
  source = "../../../terraform//blocks/common-lambda-layer-upload"
}

include "root" {
  path = find_in_parent_folders()
}

inputs = {
  prefix         = dependency.items_infra.outputs.prefix
  layer_zip_path = "${local.helper_vars.locals.deploy_dir}/common-lambda.zip"
}

dependency "items_infra" {
  config_path = "../items-infra"
}

locals {
  helper_vars = read_terragrunt_config(find_in_parent_folders("helpers_env.hcl"))
}
