module "lambda_get" {
  providers = {
    aws = aws
  }

  source = "../../modules/lambda_function/"

  lambda_zip_path = var.lambda_zip_path
  function_name   = "${var.prefix}-items-get"
  handler         = "items/get.get"
  environment = {
    DYNAMO_DB = var.dynamodb_name
  }
  additional_policy_arns = { ddb_access = aws_iam_policy.ddb_access.arn }
}

module "gateway_get" {
  providers = {
    aws = aws
  }

  source = "../../modules/api_gateway_lambda_mapping/"

  api_id            = var.api_id
  api_authorizer_id = var.api_authorizer_id
  api_execution_arn = var.api_execution_arn
  function_arn      = module.lambda_get.function_arn
  function_name     = module.lambda_get.function_name
  method            = "GET"
  path              = "/jobs"
}
