resource "aws_lambda_function" "schedule_queue" {
  filename         = var.lambda_zip_path
  function_name    = "${var.prefix}-schedule-queue-adder"
  role             = aws_iam_role.schedule_queue.arn
  handler          = "items/schedule_queue.add"
  runtime          = "python3.9"
  source_code_hash = filebase64sha256(var.lambda_zip_path)
  environment {
    variables = {
      OUTPUT_FIFO_SQS_URL = var.output_sqs_url
    }
  }
  timeout    = 6
  depends_on = [aws_cloudwatch_log_group.schedule_queue]
}

resource "aws_cloudwatch_log_group" "schedule_queue" {
  name              = "/aws/lambda/${var.prefix}-schedule-queue-adder"
  retention_in_days = 14
}
resource "aws_iam_role" "schedule_queue" {
  assume_role_policy = jsonencode(
    {
      "Version" = "2012-10-17",
      "Statement" = [
        {
          "Action" = "sts:AssumeRole",
          "Principal" = {
            "Service" = "lambda.amazonaws.com"
          },
          "Effect" = "Allow",
          "Sid"    = ""
        }
      ]
  })
  inline_policy {
    name   = "schedule-queue-lambda"
    policy = data.aws_iam_policy_document.schedule_queue.json
  }

}

data "aws_iam_policy_document" "schedule_queue" {
  statement {
    actions = [
      "logs:CreateLogStream",
      "logs:CreateLogGroup"
    ]
    resources = ["arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${var.prefix}*:*"]
  }

  statement {
    actions = [
      "logs:PutLogEvents"
    ]
    resources = [
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${var.prefix}*:*:*"
    ]
  }

  statement {
    actions = [
      "dynamodb:GetRecords",
      "dynamodb:GetShardIterator",
      "dynamodb:DescribeStream",
      "dynamodb:ListStreams"
    ]
    resources = [
      var.dynamodb_stream_arn
    ]
  }

  statement {
    actions = [
      "sqs:SendMessage"
    ]
    resources = [
      var.output_sqs_arn
    ]
  }
}

resource "aws_lambda_event_source_mapping" "schedule_queue" {
  event_source_arn  = var.dynamodb_stream_arn
  function_name     = aws_lambda_function.schedule_queue.arn
  starting_position = "LATEST"
}
