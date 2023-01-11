resource "aws_s3_object" "front_upload" {
  for_each = fileset("${path.module}/../../front/build/", "**")

  bucket = var.front_bucket_name
  key    = each.value
  source = "${path.module}/../../front/build/${each.value}"
  etag   = filemd5("${path.module}/../../front/build/${each.value}")
}
