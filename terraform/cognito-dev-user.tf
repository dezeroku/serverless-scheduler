resource "aws_cognito_user" "dev_user" {
  count          = var.cognito_dev_user_enable ? 1 : 0
  user_pool_id   = aws_cognito_user_pool.pool.id
  username       = var.cognito_dev_user_email
  password       = var.cognito_dev_user_password
  message_action = "SUPPRESS"
  attributes = {
    email = var.cognito_dev_user_email
  }
}
