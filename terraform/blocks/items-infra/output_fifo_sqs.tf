module "output_fifo_sqs" {
  providers = {
    aws = aws
  }

  source = "../../modules/items-output-fifo-sqs/"

  prefix              = local.prefix
  dynamodb_stream_arn = module.dynamodb.stream_arn
  lambda_zip_path     = var.copier_lambda_zip_path
}
