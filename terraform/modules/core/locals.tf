locals {
  prefix      = "${var.service}-${var.stage}"
  auth_domain = "auth.${var.front_domain}"
}
