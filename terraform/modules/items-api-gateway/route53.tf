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
