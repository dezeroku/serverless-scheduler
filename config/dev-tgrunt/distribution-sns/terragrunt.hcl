terraform {
  source = "../../../terraform//blocks/distribution-sns"
}

include "root" {
  path = find_in_parent_folders()
}

inputs = {
  sns_topic_name = "${dependency.items_infra.outputs.prefix}-distribution"
}

dependency "items_infra" {
  config_path = "../items-infra"
}
