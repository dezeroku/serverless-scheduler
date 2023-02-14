module "front_upload" {
  providers = {
    aws = aws
  }

  source = "../../modules/front/"

  front_bucket_name = var.front_bucket_name
}
