output "sns_topic_arn" {
  value = aws_sns_topic.distribution.arn
}

output "sns_topic_name" {
  value = aws_sns_topic.distribution.name
}
