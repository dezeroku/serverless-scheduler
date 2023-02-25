module "lambda_schedule_queue" {
  providers = {
    aws = aws
  }

  source = "../../modules/lambda_function/"

  lambda_zip_path = var.lambda_zip_path
  function_name   = "${var.prefix}-schedule-queue-adder"
  handler         = "items/schedule_queue.add"
  environment = {
    OUTPUT_FIFO_SQS_URL = var.output_sqs_url
  }
  additional_policy_arns = { schedule_queue = aws_iam_policy.schedule_queue.arn }
}

resource "aws_lambda_event_source_mapping" "schedule_queue" {
  event_source_arn  = var.dynamodb_stream_arn
  function_name     = module.lambda_schedule_queue.function_arn
  starting_position = "LATEST"
}
