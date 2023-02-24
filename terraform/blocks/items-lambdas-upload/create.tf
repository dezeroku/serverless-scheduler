resource "aws_lambda_function" "items_create" {
  filename         = var.lambda_zip_path
  function_name    = "${var.prefix}-item-create"
  role             = aws_iam_role.items.arn
  handler          = "items/create.create"
  runtime          = "python3.9"
  source_code_hash = filebase64sha256(var.lambda_zip_path)
  environment {
    variables = {
      DYNAMO_DB = var.dynamodb_name
    }
  }
  timeout    = 6
  depends_on = [aws_cloudwatch_log_group.items_create]
}

resource "aws_cloudwatch_log_group" "items_create" {
  name              = "/aws/lambda/${var.prefix}-item-create"
  retention_in_days = 14
}

resource "aws_apigatewayv2_integration" "items_create" {
  api_id           = var.api_id
  integration_type = "AWS_PROXY"

  integration_method     = "POST"
  integration_uri        = aws_lambda_function.items_create.arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "items_create" {
  authorization_type = "JWT"
  api_id             = var.api_id
  route_key          = "POST /item/create"
  authorizer_id      = var.api_authorizer_id

  target = "integrations/${aws_apigatewayv2_integration.items_create.id}"
}

resource "aws_lambda_permission" "items_create" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.items_create.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*"
}
