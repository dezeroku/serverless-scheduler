resource "aws_cognito_user_pool" "pool" {
  name                     = var.pool_name
  username_attributes      = ["email"]
  auto_verified_attributes = ["email"]

  deletion_protection = var.deletion_protection

  password_policy {
    # Dummy settings for development
    minimum_length                   = 8
    require_numbers                  = false
    require_symbols                  = false
    require_uppercase                = false
    temporary_password_validity_days = 7
  }

  admin_create_user_config {
    allow_admin_create_user_only = true
  }

  account_recovery_setting {
    recovery_mechanism {
      name     = "verified_email"
      priority = 1
    }
  }
}
