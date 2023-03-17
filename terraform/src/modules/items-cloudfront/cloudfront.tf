resource "aws_cloudfront_distribution" "front_distribution" {
  origin {
    domain_name = var.front_bucket_regional_domain_name
    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.front_bucket.cloudfront_access_identity_path
    }
    origin_id = "front-s3"
  }

  restrictions {
    geo_restriction {
      locations        = []
      restriction_type = "none"
    }
  }

  custom_error_response {
    error_code         = 403
    response_code      = 200
    response_page_path = "/index.html"

  }

  enabled             = true
  default_root_object = "index.html"

  aliases = [var.front_domain]

  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "front-s3"

    # CachingOptimized - https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/using-managed-cache-policies.html
    #cache_policy_id = "658327ea-f89d-4fab-a63d-7e88639e58f6"
    # Caching Disable - temporarily
    cache_policy_id        = "4135ea2d-6df8-44a3-9df3-4b5a84be39ad"
    viewer_protocol_policy = "redirect-to-https"
    compress               = true
    #min_ttl                = 0
    #default_ttl            = 3600
    #max_ttl                = 86400
  }

  price_class = "PriceClass_100"

  viewer_certificate {
    acm_certificate_arn      = module.front_domain_cert.certificate_arn
    minimum_protocol_version = "TLSv1.2_2019"
    ssl_support_method       = "sni-only"
  }
}
