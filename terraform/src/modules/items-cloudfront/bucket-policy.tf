resource "aws_cloudfront_origin_access_identity" "front_bucket" {
  comment = "FrontBucket origin identity"
}

resource "aws_s3_bucket_policy" "allow_access_from_cloudfront_origin" {
  bucket = var.front_bucket_id
  policy = data.aws_iam_policy_document.allow_access_from_cloudfront_origin.json
}

data "aws_iam_policy_document" "allow_access_from_cloudfront_origin" {
  statement {
    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.front_bucket.iam_arn]
    }

    actions = [
      "s3:GetObject"
    ]

    resources = [
      "${var.front_bucket_arn}/*"
    ]
  }
}
