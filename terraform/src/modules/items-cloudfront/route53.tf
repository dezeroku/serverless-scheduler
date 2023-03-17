resource "aws_route53_record" "front-cloudfront" {
  name    = var.front_domain
  type    = "A"
  zone_id = data.aws_route53_zone.cert_zone.zone_id
  alias {
    evaluate_target_health = false
    name                   = aws_cloudfront_distribution.front_distribution.domain_name
    # This zone_id is fixed
    zone_id = "Z2FDTNDATAQYW2"
  }
}
