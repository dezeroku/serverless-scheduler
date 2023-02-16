module "items_core" {
  providers = {
    aws     = aws
    aws.acm = aws.acm
  }

  source = "../../blocks/items-infra/"

  stage                       = var.stage
  service                     = var.service
  api_domain                  = var.api_domain
  front_domain                = var.front_domain
  route53_cert_zone           = var.route53_cert_zone
  api_gateway_api_mapping_key = var.api_gateway_api_mapping_key
  cognito_deletion_protection = var.cognito_deletion_protection
  cognito_dev_user_enable     = var.cognito_dev_user_enable
  cognito_dev_user_email      = var.cognito_dev_user_email
  cognito_dev_user_password   = var.cognito_dev_user_password
}
