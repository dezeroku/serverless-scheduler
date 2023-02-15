module "front_upload" {
  providers = {
    aws = aws
  }

  source = "../../blocks/front-upload/"

  front_bucket_name = var.front_bucket_name
}
