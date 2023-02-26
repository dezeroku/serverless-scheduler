module "lambda_schedule_controller" {
  providers = {
    aws = aws
  }

  source = "../../modules/lambda_function/"

  lambda_zip_path = var.lambda_zip_path
  function_name   = "${var.prefix}-schedulers-schedule-controller"
  handler         = "schedulers/schedule_controller.schedule_controller"
  environment = {
    DISTRIBUTION_SNS_TOPIC_ARN = var.distribution_sns_topic_arn
    SCHEDULERS_GROUP           = aws_scheduler_schedule_group.group.id
    SCHEDULERS_ROLE_ARN        = aws_iam_role.scheduler_execution.arn
  }
  additional_policy_arns = { sqs_access = aws_iam_policy.schedule_controller_sqs.arn,
    scheduler_access = aws_iam_policy.schedule_controller_scheduler.arn,
  pass_role = aws_iam_policy.schedule_controller_pass_role.arn }
  # Max batch-size=10, let's allow 6 seconds per execution
  timeout = 60
}

resource "aws_lambda_event_source_mapping" "schedule_queue" {
  event_source_arn        = var.input_sqs_queue_arn
  function_name           = module.lambda_schedule_controller.function_arn
  function_response_types = ["ReportBatchItemFailures"]
  scaling_config {
    # Up to 5 concurrent lambdas
    # This equals to max 50 items being processed at the same time
    # Let's treat it as training wheels to not cause an insane cost
    maximum_concurrency = 5
  }
}
