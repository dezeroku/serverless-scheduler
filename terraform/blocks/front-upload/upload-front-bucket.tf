# "Smart" MIME thanks to https://engineering.statefarm.com/blog/terraform-s3-upload-with-mime/

locals {
  mime_types = jsondecode(file("${path.module}/mime.json"))
}

resource "aws_s3_object" "front_upload" {
  for_each = fileset("${path.module}/../../../front/build/", "**")

  bucket = var.front_bucket_name
  key    = each.value
  source = "${path.module}/../../../front/build/${each.value}"

  etag         = filemd5("${path.module}/../../../front/build/${each.value}")
  content_type = lookup(local.mime_types, replace(regex("\\.[^.]+$", each.value), ".", ""), null)
}
