module "cloudfront" {
  providers = {
    aws     = aws
    aws.acm = aws.acm
  }

  source = "../../modules/items-cloudfront/"

  front_domain                      = var.front_domain
  route53_cert_zone                 = var.route53_cert_zone
  front_bucket_regional_domain_name = module.front_bucket.bucket_regional_domain_name
  front_bucket_id                   = module.front_bucket.bucket_id
  front_bucket_arn                  = module.front_bucket.bucket_arn
}
