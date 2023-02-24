resource "aws_lambda_function" "items_update" {
  filename         = var.lambda_zip_path
  function_name    = "${var.prefix}-item-update"
  role             = aws_iam_role.items.arn
  handler          = "items/update.update"
  runtime          = "python3.9"
  source_code_hash = filebase64sha256(var.lambda_zip_path)
  environment {
    variables = {
      DYNAMO_DB = var.dynamodb_name
    }
  }
  timeout    = 6
  depends_on = [aws_cloudwatch_log_group.items_update]
}

resource "aws_cloudwatch_log_group" "items_update" {
  name              = "/aws/lambda/${var.prefix}-item-update"
  retention_in_days = 14
}

resource "aws_apigatewayv2_integration" "items_update" {
  api_id           = var.api_id
  integration_type = "AWS_PROXY"

  integration_method     = "PUT"
  integration_uri        = aws_lambda_function.items_update.arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "items_update" {
  authorization_type = "JWT"
  api_id             = var.api_id
  route_key          = "PUT /item/update/{item_id}"
  authorizer_id      = var.api_authorizer_id

  target = "integrations/${aws_apigatewayv2_integration.items_update.id}"
}

resource "aws_lambda_permission" "items_update" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.items_update.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*"
}
