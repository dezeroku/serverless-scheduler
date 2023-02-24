output "prefix" {
  value = local.prefix
}

output "base_domain" {
  value = var.route53_cert_zone
}

output "api_domain" {
  value = var.api_domain
}

output "auth_domain" {
  value = local.auth_domain
}

output "front_domain" {
  value = var.front_domain
}

output "items_dynamodb_name" {
  value = module.dynamodb.table_name
}

output "items_dynamodb_stream_arn" {
  value = module.dynamodb.stream_arn
}

output "api_domain_cert_arn" {
  value = module.api_gateway.api_domain_cert_arn
}

output "front_domain_cert_arn" {
  value = module.cloudfront.domain_cert_arn
}

output "auth_domain_cert_arn" {
  value = module.cognito.auth_domain_cert_arn
}

output "api_gateway_id" {
  value = module.api_gateway.api_id
}

output "api_gateway_execution_arn" {
  value = module.api_gateway.api_execution_arn
}

output "cognito_authorizer_id" {
  value = module.api_gateway.cognito_authorizer_id
}

output "cognito_user_pool_client_id" {
  value = module.cognito.client_id
}

output "front_bucket_id" {
  value = module.front_bucket.bucket_id
}

output "output_sqs_url" {
  value = module.output_fifo_sqs.output_sqs_url
}

output "output_sqs_arn" {
  value = module.output_fifo_sqs.output_sqs_arn
}
