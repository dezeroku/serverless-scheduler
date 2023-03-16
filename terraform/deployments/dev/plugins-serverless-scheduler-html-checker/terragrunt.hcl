include "root" {
  path = find_in_parent_folders()
}

include "env" {
  path = "${get_terragrunt_dir()}/../../../../plugins/serverless-scheduler-html-checker/terraform/terragrunt.hcl"
}
