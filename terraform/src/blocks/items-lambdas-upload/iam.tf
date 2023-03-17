resource "aws_iam_policy" "ddb_access" {
  policy = data.aws_iam_policy_document.ddb_access.json
}

data "aws_iam_policy_document" "ddb_access" {
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

resource "aws_iam_policy" "schedule_queue" {
  policy = data.aws_iam_policy_document.schedule_queue.json
}

data "aws_iam_policy_document" "schedule_queue" {
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
