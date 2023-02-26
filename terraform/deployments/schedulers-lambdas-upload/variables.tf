variable "aws_region" {
  type = string
}

variable "stage" {
  type = string
}

variable "service" {
  type = string
}

variable "prefix" {
  type = string
}

variable "lambda_zip_path" {
  type = string
}

variable "input_sqs_queue_arn" {
  type = string
}

variable "distribution_sns_topic_arn" {
  type = string
}

variable "schedulers_group" {
  type = string
}
