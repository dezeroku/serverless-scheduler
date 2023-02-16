module "auth_domain_cert" {
  providers = {
    aws = aws.acm
  }

  source = "../../modules/acm_certificate/"

  domain            = var.auth_domain
  route53_cert_zone = var.route53_cert_zone
}
