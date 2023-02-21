resource "aws_dynamodb_table" "items" {
  name             = var.table_name
  billing_mode     = "PAY_PER_REQUEST"
  stream_enabled   = true
  stream_view_type = "NEW_IMAGE"

  hash_key  = "user_email"
  range_key = "job_id"

  attribute {
    name = "user_email"
    type = "S"
  }

  attribute {
    name = "job_id"
    type = "N"
  }
}
