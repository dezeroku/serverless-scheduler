output "api_domain_cert_arn" {
  value = module.api_domain_cert.certificate_arn
}

output "api_id" {
  value = aws_apigatewayv2_api.api.id
}

output "api_execution_arn" {
  value = aws_apigatewayv2_api.api.execution_arn
}

output "cognito_authorizer_id" {
  value = aws_apigatewayv2_authorizer.cognito.id
}

output "api_mapping_key" {
  value = var.api_mapping_key
}
