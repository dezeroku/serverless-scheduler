module "lambda_update" {
  providers = {
    aws = aws
  }

  source = "../../modules/lambda_function/"

  lambda_zip_path = var.lambda_zip_path
  function_name   = "${var.prefix}-item-update"
  handler         = "items/update.update"
  environment = {
    DYNAMO_DB = var.dynamodb_name
  }
  additional_policy_arns = { ddb_access = aws_iam_policy.ddb_access.arn }
  layer_arns             = [var.common_layer_arn]
}

module "gateway_update" {
  providers = {
    aws = aws
  }

  source = "../../modules/api_gateway_lambda_mapping/"

  api_id            = var.api_id
  api_authorizer_id = var.api_authorizer_id
  api_execution_arn = var.api_execution_arn
  function_arn      = module.lambda_update.function_arn
  function_name     = module.lambda_update.function_name
  method            = "PUT"
  path              = "/job/update/{job_id}"
}
