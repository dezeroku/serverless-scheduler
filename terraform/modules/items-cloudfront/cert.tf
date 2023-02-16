module "front_domain_cert" {
  providers = {
    aws = aws.acm
  }

  source = "../acm_certificate/"

  domain            = var.front_domain
  route53_cert_zone = var.route53_cert_zone
}

data "aws_route53_zone" "cert_zone" {
  name         = var.route53_cert_zone
  private_zone = false
}
