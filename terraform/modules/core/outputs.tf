output "items_dynamodb_name" {
  value = aws_dynamodb_table.items.name
}

output "prefix" {
  value = local.prefix
}

output "base_domain" {
  value = var.route53_cert_zone
}

output "api_domain" {
  value = var.api_domain
}

output "api_domain_cert_arn" {
  value = module.api_domain_cert.certificate_arn
}

output "front_domain" {
  value = var.front_domain
}

output "front_domain_cert_arn" {
  value = module.front_domain_cert.certificate_arn
}

output "auth_domain" {
  value = local.auth_domain
}

output "auth_domain_cert_arn" {
  value = module.auth_domain_cert.certificate_arn
}

output "api_gateway_id" {
  value = aws_apigatewayv2_api.api.id
}

output "cognito_authorizer_id" {
  value = aws_apigatewayv2_authorizer.cognito.id
}

output "cognito_user_pool_client_id" {
  value = aws_cognito_user_pool_client.client.id
}

output "front_bucket_id" {
  value = aws_s3_bucket.front_bucket.id
}
