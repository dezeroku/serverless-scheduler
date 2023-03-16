terraform {
  source = "../../../terraform//blocks/items-lambdas-upload"
}

include "root" {
  path = find_in_parent_folders()
}

inputs = {
  prefix              = dependency.items_infra.outputs.prefix
  api_id              = dependency.items_infra.outputs.api_gateway_id
  api_execution_arn   = dependency.items_infra.outputs.api_gateway_execution_arn
  api_authorizer_id   = dependency.items_infra.outputs.cognito_authorizer_id
  common_layer_arn    = dependency.common_lambda_layer.outputs.layer_arn
  plugins_layer_arn   = dependency.plugins_lambda_layer.outputs.layer_arn
  lambda_zip_path     = "${local.helper_vars.locals.deploy_dir}/items-lambda.zip"
  dynamodb_name       = dependency.items_infra.outputs.items_dynamodb_name
  dynamodb_stream_arn = dependency.items_infra.outputs.items_dynamodb_stream_arn
  output_sqs_arn      = dependency.items_infra.outputs.output_sqs_arn
  output_sqs_url      = dependency.items_infra.outputs.output_sqs_url
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

locals {
  helper_vars = read_terragrunt_config(find_in_parent_folders("helpers_env.hcl"))
}
