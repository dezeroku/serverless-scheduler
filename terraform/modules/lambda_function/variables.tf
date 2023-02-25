variable "environment" {
  type    = map(string)
  default = {}
}

variable "function_name" {
  type = string
}

variable "runtime" {
  type    = string
  default = "python3.9"
}

variable "handler" {
  type = string
}

variable "lambda_zip_path" {
  type = string
}

variable "timeout" {
  type    = number
  default = 6
}

variable "additional_policy_arns" {
  type    = map(string)
  default = {}
  # e.g. {access = "some_arn"}
}
