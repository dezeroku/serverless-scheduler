resource "aws_cognito_user_pool_domain" "main" {
  # Set up cloudfront first to make sure that A record for parent domain is in place
  domain          = var.auth_domain
  certificate_arn = module.auth_domain_cert.certificate_arn
  user_pool_id    = aws_cognito_user_pool.pool.id
}

data "aws_route53_zone" "cert_zone" {
  name         = var.route53_cert_zone
  private_zone = false
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
