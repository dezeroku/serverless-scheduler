module "cloudfront" {
  providers = {
    aws     = aws
    aws.acm = aws.acm
  }

  source = "../../modules/items-cloudfront/"

  front_domain                                 = var.front_domain
  route53_cert_zone                            = var.route53_cert_zone
  front_bucket_regional_domain_name            = aws_s3_bucket.front_bucket.bucket_regional_domain_name
  front_bucket_cloudfront_access_identity_path = aws_cloudfront_origin_access_identity.front_bucket.cloudfront_access_identity_path
}
