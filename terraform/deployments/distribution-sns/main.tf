module "distribution_sns" {
  providers = {
    aws = aws
  }

  source = "../../blocks/distribution-sns/"

  sns_topic_name = "${var.prefix}-distribution"
}
