module "front_upload" {
  providers = {
    aws = aws
  }

  source = "../../blocks/items-front-upload/"

  front_bucket_name = var.front_bucket_name
  build_dir_path    = var.build_dir_path
}
