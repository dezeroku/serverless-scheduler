resource "aws_acm_certificate" "api_domain" {
  provider = aws.acm
  domain_name       = var.api_domain
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

data "aws_route53_zone" "cert_zone" {
  name         = var.route53_cert_zone
  private_zone = false
}

resource "aws_route53_record" "api_domain_cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.api_domain.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = data.aws_route53_zone.cert_zone.zone_id
}

resource "aws_acm_certificate_validation" "api_domain" {
  provider = aws.acm
  certificate_arn         = aws_acm_certificate.api_domain.arn
  validation_record_fqdns = [for record in aws_route53_record.api_domain_cert_validation : record.fqdn]
}
