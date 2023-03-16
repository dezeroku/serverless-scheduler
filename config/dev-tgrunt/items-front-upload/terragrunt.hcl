terraform {
  source = "../../../terraform//blocks/items-front-upload"
}

include "root" {
  path = find_in_parent_folders()
}

inputs = {
    front_bucket_name=dependency.items_infra.outputs.front_bucket_id
    build_dir_path="${local.helper_vars.locals.deploy_dir}/front/"
}

dependency "items_infra" {
    config_path = "../items-infra"
}

locals {
  helper_vars = read_terragrunt_config(find_in_parent_folders("helpers_env.hcl"))
}
