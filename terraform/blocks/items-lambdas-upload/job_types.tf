module "lambda_job_types" {
  providers = {
    aws = aws
  }

  source = "../../modules/lambda_function/"

  lambda_zip_path = var.lambda_zip_path
  function_name   = "${var.prefix}-items-job-types"
  handler         = "items/job_types.get"
  layer_arns = [
    var.common_layer_arn,
    var.plugins_layer_arn
  ]
}

module "gateway_job_types" {
  providers = {
    aws = aws
  }

  source = "../../modules/api_gateway_lambda_mapping/"

  api_id            = var.api_id
  api_authorizer_id = var.api_authorizer_id
  api_execution_arn = var.api_execution_arn
  function_arn      = module.lambda_job_types.function_arn
  function_name     = module.lambda_job_types.function_name
  method            = "GET"
  path              = "/job_types"
}
