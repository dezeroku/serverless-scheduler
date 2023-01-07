output "items_dynamodb_name" {
  value = aws_dynamodb_table.items.name
}

output "service" {
  value = var.service
}

output "stage" {
  value = var.stage
}

output "aws_region" {
  value = var.aws_region
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
