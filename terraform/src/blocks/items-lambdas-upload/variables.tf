variable "prefix" {
  type = string
}

variable "api_id" {
  type = string
}

variable "api_execution_arn" {
  type = string
}

variable "api_authorizer_id" {
  type = string
}

variable "common_layer_arn" {
  type = string
}

variable "plugins_layer_arn" {
  type = string
}

variable "lambda_zip_path" {
  type = string
}

variable "dynamodb_name" {
  type = string
}

variable "output_sqs_url" {
  type = string
}

variable "output_sqs_arn" {
  type = string
}

variable "dynamodb_stream_arn" {
  type = string
}
