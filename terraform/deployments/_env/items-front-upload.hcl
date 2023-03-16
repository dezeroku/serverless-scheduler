terraform {
  source = "../../..//blocks/items-front-upload"

  before_hook "apply_pool_id" {
    commands = ["apply", "plan"]
    execute  = ["sed", "-i", "s/CLIENT_POOL_ID: \".*\"/CLIENT_POOL_ID: \"${dependency.items_infra.outputs.cognito_user_pool_client_id}\"/", "${local.helper_vars.locals.deploy_dir}/front/env-config.js"]
  }
}

inputs = {
  front_bucket_name = dependency.items_infra.outputs.front_bucket_id
  build_dir_path    = "${local.helper_vars.locals.deploy_dir}/front/"
}

dependency "items_infra" {
  config_path = "../items-infra"
}

locals {
  helper_vars = read_terragrunt_config(find_in_parent_folders("helpers_env.hcl"))
}
