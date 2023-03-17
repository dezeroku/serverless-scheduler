resource "aws_apigatewayv2_integration" "integration" {
  api_id           = var.api_id
  integration_type = "AWS_PROXY"

  integration_method     = var.method
  integration_uri        = var.function_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "route" {
  authorization_type = "JWT"
  api_id             = var.api_id
  route_key          = "${var.method} ${var.path}"
  authorizer_id      = var.api_authorizer_id

  target = "integrations/${aws_apigatewayv2_integration.integration.id}"
}

resource "aws_lambda_permission" "permission" {
  action        = "lambda:InvokeFunction"
  function_name = var.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*"
}
