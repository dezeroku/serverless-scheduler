resource "aws_apigatewayv2_api" "api" {
  name                         = var.api_name
  protocol_type                = "HTTP"
  disable_execute_api_endpoint = true
  cors_configuration {
    # This is same as cors = true in serverless
    allow_credentials = false
    allow_origins     = ["*"]
    allow_headers = ["Content-Type",
      "X-Amz-Date",
      "Authorization",
      "X-Api-Key",
      "X-Amz-Security-Token",
      "X-Amz-User-Agent",
      "X-Amzn-Trace-Id"
    ]
    allow_methods = ["OPTIONS", "GET", "POST", "PUT", "DELETE"]
    max_age       = 300
  }
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.api.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_apigatewayv2_api_mapping" "mapping" {
  api_id          = aws_apigatewayv2_api.api.id
  domain_name     = aws_apigatewayv2_domain_name.api.id
  stage           = aws_apigatewayv2_stage.default.id
  api_mapping_key = var.api_mapping_key
}

resource "aws_apigatewayv2_domain_name" "api" {
  domain_name = var.api_domain
  domain_name_configuration {
    certificate_arn = module.api_domain_cert.certificate_arn
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }
}
