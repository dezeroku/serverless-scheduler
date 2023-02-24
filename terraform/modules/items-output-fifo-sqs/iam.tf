data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

resource "aws_iam_role" "copier" {
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
    policy = data.aws_iam_policy_document.copier.json
  }

}

data "aws_iam_policy_document" "copier" {
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
      aws_sqs_queue.output.arn
    ]
  }
}
