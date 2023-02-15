# This needs to be changed to us-east-1 if api-gateway-domain is ever changed from "regional"
module "api_domain_cert" {
  source = "../../modules/acm_certificate/"

  domain            = var.api_domain
  route53_cert_zone = var.route53_cert_zone
}

resource "aws_apigatewayv2_authorizer" "cognito" {
  api_id           = aws_apigatewayv2_api.api.id
  authorizer_type  = "JWT"
  identity_sources = ["$request.header.Authorization"]
  name             = "${local.prefix}-cognito-authorizer"

  jwt_configuration {
    # CognitoUserPoolClient
    audience = [aws_cognito_user_pool_client.client.id]
    # CognitoUserPool
    issuer = "https://${aws_cognito_user_pool.pool.endpoint}"
  }
}

resource "aws_apigatewayv2_api" "api" {
  name                         = local.prefix
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

resource "aws_apigatewayv2_api_mapping" "example" {
  api_id          = aws_apigatewayv2_api.api.id
  domain_name     = aws_apigatewayv2_domain_name.api.id
  stage           = aws_apigatewayv2_stage.default.id
  api_mapping_key = var.api_gateway_api_mapping_key
}

resource "aws_apigatewayv2_domain_name" "api" {
  domain_name = var.api_domain
  domain_name_configuration {
    certificate_arn = module.api_domain_cert.certificate_arn
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }
}

data "aws_route53_zone" "api_gateway_zone" {
  name         = var.route53_cert_zone
  private_zone = false
}

resource "aws_route53_record" "api_gateway_domain" {
  name    = aws_apigatewayv2_domain_name.api.domain_name
  type    = "A"
  zone_id = data.aws_route53_zone.api_gateway_zone.id

  alias {
    evaluate_target_health = true
    name                   = aws_apigatewayv2_domain_name.api.domain_name_configuration[0].target_domain_name
    zone_id                = aws_apigatewayv2_domain_name.api.domain_name_configuration[0].hosted_zone_id
  }
}
