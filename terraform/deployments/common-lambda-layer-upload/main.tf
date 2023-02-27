module "layer_upload" {
  providers = {
    aws = aws
  }

  source = "../../blocks/common-lambda-layer-upload/"

  prefix          = var.prefix
  layer_zip_path  = var.layer_zip_path
  keep_old_layers = var.keep_old_layers
}
