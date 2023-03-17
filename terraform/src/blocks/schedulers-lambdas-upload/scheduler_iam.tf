resource "aws_iam_role" "scheduler_execution" {
  assume_role_policy = jsonencode(
    {
      "Version" = "2012-10-17",
      "Statement" = [
        {
          "Action" = "sts:AssumeRole",
          "Principal" = {
            "Service" = "scheduler.amazonaws.com"
          },
          "Effect" = "Allow",
          "Sid"    = ""
        }
      ]
  })

  managed_policy_arns = [aws_iam_policy.schedule_controller_sns.arn]
}
