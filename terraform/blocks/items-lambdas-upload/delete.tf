resource "aws_lambda_function" "items_delete" {
  filename         = var.lambda_zip_path
  function_name    = "${var.prefix}-item-delete"
  role             = aws_iam_role.items.arn
  handler          = "items/delete.delete"
  runtime          = "python3.8"
  source_code_hash = filebase64sha256(var.lambda_zip_path)
  environment {
    variables = {
      DYNAMO_DB = var.dynamodb_name
    }
  }
  timeout    = 6
  depends_on = [aws_cloudwatch_log_group.items_delete]
}

resource "aws_cloudwatch_log_group" "items_delete" {
  name              = "/aws/lambda/${var.prefix}-item-delete"
  retention_in_days = 14
}

resource "aws_apigatewayv2_integration" "items_delete" {
  api_id           = var.api_id
  integration_type = "AWS_PROXY"

  integration_method     = "DELETE"
  integration_uri        = aws_lambda_function.items_delete.arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "items_delete" {
  authorization_type = "JWT"
  api_id             = var.api_id
  route_key          = "DELETE /item/delete/{item_id}"
  authorizer_id      = var.api_authorizer_id

  target = "integrations/${aws_apigatewayv2_integration.items_delete.id}"
}

resource "aws_lambda_permission" "items_delete" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.items_delete.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*"
}
