resource "aws_cognito_user_pool_client" "client" {
  name         = var.client_name
  user_pool_id = aws_cognito_user_pool.pool.id

  callback_urls                        = ["https://${var.front_domain}/login/cognito-parser"]
  default_redirect_uri                 = "https://${var.front_domain}/login/cognito-parser"
  logout_urls                          = ["https://${var.front_domain}/logout"]
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_flows                  = ["code", "implicit"]
  allowed_oauth_scopes                 = ["email", "openid", "profile"]
  supported_identity_providers         = ["COGNITO"]
  generate_secret                      = false
}
