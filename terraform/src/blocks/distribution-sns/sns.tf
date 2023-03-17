resource "aws_sns_topic" "distribution" {
  name = var.sns_topic_name

  lambda_failure_feedback_role_arn = aws_iam_role.failure_delivery_logging.arn
}
