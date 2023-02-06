resource "aws_dynamodb_table" "items" {
  name         = "${local.prefix}-items"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "user_email"
  range_key    = "job_id"

  attribute {
    name = "user_email"
    type = "S"
  }

  attribute {
    name = "job_id"
    type = "N"
  }
}
