resource "aws_apigatewayv2_authorizer" "cognito" {
  api_id           = aws_apigatewayv2_api.api.id
  authorizer_type  = "JWT"
  identity_sources = ["$request.header.Authorization"]
  name             = var.cognito_authorizer_name

  jwt_configuration {
    # CognitoUserPoolClient
    audience = [
      var.cognito_user_pool_client_id
    ]
    # CognitoUserPool
    issuer = "https://${var.cognito_user_pool_endpoint}"
  }
}
