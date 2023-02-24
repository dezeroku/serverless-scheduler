resource "aws_lambda_function" "items_get" {
  filename         = var.lambda_zip_path
  function_name    = "${var.prefix}-items-get"
  role             = aws_iam_role.items.arn
  handler          = "items/get.get"
  runtime          = "python3.9"
  source_code_hash = filebase64sha256(var.lambda_zip_path)
  environment {
    variables = {
      DYNAMO_DB = var.dynamodb_name
    }
  }
  timeout    = 6
  depends_on = [aws_cloudwatch_log_group.items_get]
}

resource "aws_cloudwatch_log_group" "items_get" {
  name              = "/aws/lambda/${var.prefix}-items-get"
  retention_in_days = 14
}


resource "aws_apigatewayv2_integration" "items_get" {
  api_id           = var.api_id
  integration_type = "AWS_PROXY"

  integration_method     = "GET"
  integration_uri        = aws_lambda_function.items_get.arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "items_get" {
  authorization_type = "JWT"
  api_id             = var.api_id
  route_key          = "GET /items"
  authorizer_id      = var.api_authorizer_id

  target = "integrations/${aws_apigatewayv2_integration.items_get.id}"
}

resource "aws_lambda_permission" "items_get" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.items_get.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*"
}
