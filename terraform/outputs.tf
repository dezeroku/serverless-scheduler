output "items_dynamodb_name" {
  value = aws_dynamodb_table.items.name
}

output "api_domain" {
  value = var.api_domain
}

output "api_domain_cert_arn" {
  value = aws_acm_certificate.api_domain.arn
}
