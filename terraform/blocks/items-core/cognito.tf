module "cognito" {
  # To make sure that root A record is created first
  depends_on = [module.cloudfront]
  providers = {
    aws     = aws
    aws.acm = aws.acm
  }

  source = "../../modules/items-cognito/"

  pool_name           = local.prefix
  client_name         = "${local.prefix}-client"
  front_domain        = var.front_domain
  auth_domain         = local.auth_domain
  deletion_protection = var.cognito_deletion_protection
  route53_cert_zone   = var.route53_cert_zone
}
