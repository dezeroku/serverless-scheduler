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

variable "layer_zip_path" {
  type = string
}

variable "keep_old_layers" {
  # Lambdas that are already deployed with a layer keep access to it
  # So this should be set to true only if you want to reuse older versions of layers for new deployments
  type = bool
}
