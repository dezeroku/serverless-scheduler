module "lambdas_upload" {
  providers = {
    aws = aws
  }

  source = "../../blocks/schedulers-lambdas-upload/"

  prefix                     = var.prefix
  common_layer_arn           = var.common_layer_arn
  lambda_zip_path            = var.lambda_zip_path
  input_sqs_queue_arn        = var.input_sqs_queue_arn
  distribution_sns_topic_arn = var.distribution_sns_topic_arn
  schedulers_group           = var.schedulers_group
}
