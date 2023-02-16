module "api_gateway" {
  providers = {
    aws = aws
  }

  source = "../../modules/items-api-gateway/"

  api_domain                  = var.api_domain
  route53_cert_zone           = var.route53_cert_zone
  api_name                    = local.prefix
  cognito_authorizer_name     = "${local.prefix}-cognito-authorizer"
  cognito_user_pool_client_id = module.cognito.client_id
  cognito_user_pool_endpoint  = module.cognito.pool_endpoint
  api_mapping_key             = var.api_gateway_api_mapping_key
}
