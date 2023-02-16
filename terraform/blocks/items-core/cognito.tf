resource "aws_cognito_user_pool" "pool" {
  name                     = local.prefix
  username_attributes      = ["email"]
  auto_verified_attributes = ["email"]

  deletion_protection = var.cognito_deletion_protection

  password_policy {
    # Dummy settings for development
    minimum_length                   = 8
    require_numbers                  = false
    require_symbols                  = false
    require_uppercase                = false
    temporary_password_validity_days = 7
  }

  admin_create_user_config {
    allow_admin_create_user_only = true
  }
}

resource "aws_cognito_user_pool_client" "client" {
  name         = "${local.prefix}-client"
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

resource "aws_cognito_user_pool_domain" "main" {
  # Set up cloudfront first to make sure that A record for parent domain is in place
  depends_on      = [module.cloudfront]
  domain          = local.auth_domain
  certificate_arn = module.auth_domain_cert.certificate_arn
  user_pool_id    = aws_cognito_user_pool.pool.id
}

resource "aws_route53_record" "auth-cognito-record" {
  name    = aws_cognito_user_pool_domain.main.domain
  type    = "A"
  zone_id = data.aws_route53_zone.cert_zone.zone_id
  alias {
    evaluate_target_health = false
    name                   = aws_cognito_user_pool_domain.main.cloudfront_distribution_arn
    # This zone_id is fixed
    zone_id = "Z2FDTNDATAQYW2"
  }
}
