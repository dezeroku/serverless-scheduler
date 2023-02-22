variable "aws_region" {
  type = string
}

variable "stage" {
  type = string
}

variable "service" {
  type = string
}

variable "api_domain" {
  type = string
}

variable "front_domain" {
  type = string
}

variable "route53_cert_zone" {
  type = string
}

variable "api_gateway_api_mapping_key" {
  type = string
}

variable "cognito_deletion_protection" {
  default = "INACTIVE"
  type    = string

  validation {
    condition     = length(regexall("^(INACTIVE|ACTIVE)$", var.cognito_deletion_protection)) > 0
    error_message = "ERROR: Valid types are \"INACTIVE\" and \"ACTIVE\"!"
  }
}

variable "cognito_dev_user_enable" {
  type = bool
}

variable "cognito_dev_user_email" {
  type = string
}

variable "cognito_dev_user_password" {
  type = string
}

variable "copier_lambda_zip_path" {
  type = string
}
