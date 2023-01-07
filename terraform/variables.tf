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
  default = "api.example.com"
}

variable "front_domain" {
  default = "monitor.example.com"
}

variable "route53_cert_zone" {
  default = "example.com"
}
