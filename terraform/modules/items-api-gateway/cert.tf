# This needs to be changed to us-east-1 if api-gateway-domain is ever changed from "regional"
module "api_domain_cert" {
  source = "../acm_certificate/"

  domain            = var.api_domain
  route53_cert_zone = var.route53_cert_zone
}
