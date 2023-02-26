resource "aws_iam_policy" "schedule_controller_pass_role" {
  policy = data.aws_iam_policy_document.schedule_controller_pass_role.json
}

resource "aws_iam_policy" "schedule_controller_scheduler" {
  policy = data.aws_iam_policy_document.schedule_controller_scheduler.json
}

resource "aws_iam_policy" "schedule_controller_sqs" {
  policy = data.aws_iam_policy_document.schedule_controller_sqs.json
}

resource "aws_iam_policy" "schedule_controller_sns" {
  policy = data.aws_iam_policy_document.schedule_controller_sns.json
}

data "aws_iam_policy_document" "schedule_controller_scheduler" {
  statement {
    actions = [
      "scheduler:CreateSchedule",
      "scheduler:UpdateSchedule",
      "scheduler:DeleteSchedule",
    ]
    resources = [
      "arn:aws:scheduler:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:schedule/${var.schedulers_group}/*"
    ]
  }
}

data "aws_iam_policy_document" "schedule_controller_pass_role" {
  statement {
    actions = [
      "iam:GetRole",
      "iam:PassRole",
    ]
    resources = [
      aws_iam_role.scheduler_execution.arn
    ]
  }
}

data "aws_iam_policy_document" "schedule_controller_sqs" {
  statement {
    actions = [
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes",
    ]
    resources = [
      var.input_sqs_queue_arn
    ]
  }
}

data "aws_iam_policy_document" "schedule_controller_sns" {
  statement {
    actions = [
      "sns:Publish",
    ]
    resources = [
      var.distribution_sns_topic_arn
    ]
  }
}
