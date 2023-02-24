module "output_fifo_sqs" {
  providers = {
    aws = aws
  }

  source = "../../modules/items-output-fifo-sqs/"

  prefix = local.prefix
}
