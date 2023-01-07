output "items_dynamodb_name" {
  value = aws_dynamodb_table.items.name
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
