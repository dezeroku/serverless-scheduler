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

resource "aws_apigatewayv2_integration" "get" {
  api_id           = var.api_id
  integration_type = "AWS_PROXY"

  integration_method     = "GET"
  integration_uri        = module.lambda_get.function_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "get" {
  authorization_type = "JWT"
  api_id             = var.api_id
  route_key          = "GET /items"
  authorizer_id      = var.api_authorizer_id

  target = "integrations/${aws_apigatewayv2_integration.get.id}"
}

resource "aws_lambda_permission" "get" {
  action        = "lambda:InvokeFunction"
  function_name = module.lambda_get.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*"
}
