terraform {
  source = "../../../src//blocks/schedulers-lambdas-upload"
}

inputs = {
  prefix                     = dependency.items_infra.outputs.prefix
  common_layer_arn           = dependency.common_lambda_layer.outputs.layer_arn
  plugins_layer_arn          = dependency.plugins_lambda_layer.outputs.layer_arn
  lambda_zip_path            = "${local.helper_vars.locals.deploy_dir}/schedulers-lambda.zip"
  input_sqs_queue_arn        = dependency.items_infra.outputs.output_sqs_arn
  distribution_sns_topic_arn = dependency.distribution_sns.outputs.sns_topic_arn
  schedulers_group           = dependency.items_infra.outputs.prefix
}

dependency "items_infra" {
  config_path = "../items-infra"
}

dependency "common_lambda_layer" {
  config_path = "../common-lambda-layer-upload"
}

dependency "plugins_lambda_layer" {
  config_path = "../plugins-lambda-layer-upload"
}

dependency "distribution_sns" {
  config_path = "../distribution-sns"
}

locals {
  helper_vars = read_terragrunt_config(find_in_parent_folders("helpers_env.hcl"))
}
