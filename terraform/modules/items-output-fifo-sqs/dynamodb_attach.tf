resource "aws_lambda_event_source_mapping" "example" {
  event_source_arn  = var.dynamodb_stream_arn
  function_name     = aws_lambda_function.copier.arn
  starting_position = "LATEST"
}
