output "table_name" {
  value = aws_dynamodb_table.items.name
}

output "stream_arn" {
  value = aws_dynamodb_table.items.stream_arn
}
