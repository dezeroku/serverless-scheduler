output "prefix" {
  value = local.prefix
}

output "items_dynamodb_name" {
  value = module.dynamodb.table_name
}

output "base_domain" {
  value = var.route53_cert_zone
}

output "api_domain" {
  value = var.api_domain
}

output "api_domain_cert_arn" {
  value = module.api_gateway.api_domain_cert_arn
}

output "front_domain" {
  value = var.front_domain
}

output "front_domain_cert_arn" {
  value = module.cloudfront.domain_cert_arn
}

output "auth_domain" {
  value = local.auth_domain
}

output "auth_domain_cert_arn" {
  value = module.auth_domain_cert.certificate_arn
}

output "api_gateway_id" {
  value = module.api_gateway.api_id
}

output "cognito_authorizer_id" {
  value = module.api_gateway.cognito_authorizer_id
}

output "cognito_user_pool_client_id" {
  value = aws_cognito_user_pool_client.client.id
}

output "front_bucket_id" {
  value = module.front_bucket.bucket_id
}
