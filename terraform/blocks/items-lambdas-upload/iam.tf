data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

resource "aws_iam_role" "items" {
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
    name   = "monitor-page-dev-lambda"
    policy = data.aws_iam_policy_document.items.json
  }

}

data "aws_iam_policy_document" "items" {
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
      "dynamodb:Query",
      "dynamodb:Scan",
      "dynamodb:GetItem",
      "dynamodb:PutItem",
      "dynamodb:UpdateItem",
      "dynamodb:DeleteItem"
    ]
    resources = [
      "arn:aws:dynamodb:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:table/${var.dynamodb_name}"
    ]
  }
}
