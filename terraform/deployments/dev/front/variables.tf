variable "aws_region" {
  type = string
}

variable "stage" {
  type = string
}

variable "service" {
  type = string
}

variable "front_bucket_name" {
  type        = string
  description = "Bucket to upload the front files to"
}
