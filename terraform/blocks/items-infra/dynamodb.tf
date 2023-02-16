module "dynamodb" {
  providers = {
    aws = aws
  }

  source = "../../modules/items-dynamodb/"

  table_name = "${local.prefix}-items"
}
