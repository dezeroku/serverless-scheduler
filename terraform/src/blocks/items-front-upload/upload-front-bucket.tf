# "Smart" MIME thanks to https://engineering.statefarm.com/blog/terraform-s3-upload-with-mime/

locals {
  mime_types = jsondecode(file("${path.module}/mime.json"))
}

resource "aws_s3_object" "front_upload" {
  for_each = fileset(var.build_dir_path, "**")

  bucket = var.front_bucket_name
  key    = each.value
  source = "${var.build_dir_path}/${each.value}"

  etag         = filemd5("${var.build_dir_path}/${each.value}")
  content_type = lookup(local.mime_types, replace(regex("\\.[^.]+$", each.value), ".", ""), null)
}
