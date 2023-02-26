resource "aws_sns_topic" "distribution" {
  name = var.sns_topic_name
}
