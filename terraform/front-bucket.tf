resource "aws_s3_bucket" "front_bucket" {
}

resource "aws_s3_bucket_acl" "front_bucket_acl" {
  bucket = aws_s3_bucket.front_bucket.id
  acl    = "private"
}

resource "aws_cloudfront_origin_access_identity" "front_bucket" {
  comment = "FrontBucket origin identity"
}

resource "aws_s3_bucket_policy" "allow_access_from_cloudfront_origin" {
  bucket = aws_s3_bucket.front_bucket.id
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
      "${aws_s3_bucket.front_bucket.arn}/*"
    ]
  }
}
