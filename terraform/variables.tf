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
}
