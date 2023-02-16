output "pool_id" {
  value = aws_cognito_user_pool.pool.id
}

output "client_id" {
  value = aws_cognito_user_pool_client.client.id
}

output "pool_endpoint" {
  value = aws_cognito_user_pool.pool.endpoint
}

output "auth_domain_cert_arn" {
  value = module.auth_domain_cert.certificate_arn
}
