module "front_bucket" {
  providers = {
    aws = aws
  }

  source = "../../modules/items-front-bucket/"
}
