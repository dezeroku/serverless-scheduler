module "lambdas_upload" {
  providers = {
    aws = aws
  }

  source = "../../blocks/items-lambdas-upload/"

  prefix            = var.prefix
  api_id            = var.api_id
  api_execution_arn = var.api_execution_arn
  api_authorizer_id = var.api_authorizer_id
  lambda_zip_path   = var.lambda_zip_path
  dynamodb_name     = var.dynamodb_name
}
