resource "aws_iam_role" "lambda" {
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
}

resource "aws_iam_policy" "base" {
  policy = data.aws_iam_policy_document.base.json
}

resource "aws_iam_role_policy_attachment" "base_attach" {
  role       = aws_iam_role.lambda.name
  policy_arn = aws_iam_policy.base.arn
}

resource "aws_iam_role_policy_attachment" "additional_attach" {
  for_each   = var.additional_policy_arns
  role       = aws_iam_role.lambda.name
  policy_arn = each.value
}

data "aws_iam_policy_document" "base" {
  statement {
    actions = [
      "logs:CreateLogStream",
      "logs:CreateLogGroup"
    ]
    resources = ["arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${var.function_name}:*"]
  }

  statement {
    actions = [
      "logs:PutLogEvents"
    ]
    resources = [
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${var.function_name}:*:*"
    ]
  }
}
