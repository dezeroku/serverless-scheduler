output "api_domain_cert_arn" {
  value = module.api_domain_cert.certificate_arn
}

output "api_id" {
  value = aws_apigatewayv2_api.api.id
}

output "cognito_authorizer_id" {
  value = aws_apigatewayv2_authorizer.cognito.id
}

output "api_mapping_key" {
  value = var.api_mapping_key
}
