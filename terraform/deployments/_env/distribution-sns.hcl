terraform {
  source = "../../..//blocks/distribution-sns"
}

inputs = {
  sns_topic_name = "${dependency.items_infra.outputs.prefix}-distribution"
}

dependency "items_infra" {
  config_path = "../items-infra"
}
