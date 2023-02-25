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
}

resource "aws_apigatewayv2_integration" "update" {
  api_id           = var.api_id
  integration_type = "AWS_PROXY"

  integration_method     = "PUT"
  integration_uri        = module.lambda_update.function_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "update" {
  authorization_type = "JWT"
  api_id             = var.api_id
  route_key          = "PUT /item/update/{item_id}"
  authorizer_id      = var.api_authorizer_id

  target = "integrations/${aws_apigatewayv2_integration.update.id}"
}

resource "aws_lambda_permission" "update" {
  action        = "lambda:InvokeFunction"
  function_name = module.lambda_update.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*"
}
