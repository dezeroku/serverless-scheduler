variable "pool_name" {
  type = string
}

variable "client_name" {
  type = string
}

variable "route53_cert_zone" {
  type = string
}

variable "front_domain" {
  type = string
}

variable "auth_domain" {
  type = string
}

variable "deletion_protection" {
  type = string
  validation {
    condition     = length(regexall("^(INACTIVE|ACTIVE)$", var.deletion_protection)) > 0
    error_message = "ERROR: Valid types are \"INACTIVE\" and \"ACTIVE\"!"
  }
}
