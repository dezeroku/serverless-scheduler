resource "aws_s3_bucket" "front_bucket" {
  force_destroy = true
}

resource "aws_s3_bucket_acl" "front_bucket_acl" {
  bucket = aws_s3_bucket.front_bucket.id
  acl    = "private"
}
