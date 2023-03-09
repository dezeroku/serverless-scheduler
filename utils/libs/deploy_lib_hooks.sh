#!/usr/bin/env bash
# This is a library that's meant to be sourced

function get_tf_output_var() {
    mapping="${1}"
    component="${2}"
    file_to_read="${RUNDIR}/../.deployment-temp/${DEPLOY_ENV}/terraform/${component}-outputs.json"
    local output
    output="$(jq -r "${mapping}" < "${file_to_read}")"

    if [[ "${output}" == "null" ]]; then
        # If you want to allow 'null's just comment out this check
        echo "get_tf_output_var: could not find ${mapping} in ${file_to_read}" >&2
        sleep 3
        exit 1
    fi

    echo "${output}"
}

function plugin-terraform-common() {
    local target="${1}"
    local aws_region
    local service
    local stage
    local prefix
    local common_layer_arn
    local plugins_layer_arn
    local lambda_zip_path
    local distribution_sns_topic_arn

    aws_region="$(get_tf_output_var '.aws_region.value' 'items-infra')"
    service="$(get_tf_output_var '.service.value' 'items-infra')"
    stage="$(get_tf_output_var '.stage.value' 'items-infra')"
    prefix="$(get_tf_output_var '.items_core.value.prefix' 'items-infra')"
    common_layer_arn="$(get_tf_output_var '.layer_upload.value.layer_arn' 'common-lambda-layer-upload')"
    plugins_layer_arn="$(get_tf_output_var '.layer_upload.value.layer_arn' 'plugins-lambda-layer-upload')"
    lambda_zip_path="$(readlink -f "${DEPLOY_DIR}/${target}-lambda.zip")"
    distribution_sns_topic_arn="$(get_tf_output_var '.distribution_sns.value.sns_topic_arn' 'distribution-sns')"
    echo "-var aws_region=${aws_region} -var service=${service} -var stage=${stage} -var prefix=${prefix} -var common_layer_arn=${common_layer_arn} -var plugins_layer_arn=${plugins_layer_arn} -var lambda_zip_path=${lambda_zip_path} -var distribution_sns_topic_arn=${distribution_sns_topic_arn}"
}

function plugins-lambda-layer-upload-common() {
    local prefix
    local layer_zip_path

    prefix="$(get_tf_output_var '.items_core.value.prefix' 'items-infra')"
    layer_zip_path="$(readlink -f "${DEPLOY_DIR}/plugins-interface-lambda.zip")"
    echo "-var prefix=${prefix} -var layer_zip_path=${layer_zip_path}"
}

function plugins-lambda-layer-upload-pre-deploy-terraform() {
    plugins-lambda-layer-upload-common
}

function plugins-lambda-layer-upload-pre-destroy-terraform() {
    plugins-lambda-layer-upload-common
}

function common-lambda-layer-upload-common() {
    local prefix
    local layer_zip_path

    prefix="$(get_tf_output_var '.items_core.value.prefix' 'items-infra')"
    layer_zip_path="$(readlink -f "${DEPLOY_DIR}/common-lambda.zip")"
    echo "-var prefix=${prefix} -var layer_zip_path=${layer_zip_path}"
}

function common-lambda-layer-upload-pre-deploy-terraform() {
    common-lambda-layer-upload-common
}

function common-lambda-layer-upload-pre-destroy-terraform() {
    common-lambda-layer-upload-common
}

function schedulers-lambdas-upload-common() {
    local prefix
    local common_layer_arn
    local plugins_layer_arn
    local lambda_zip_path
    local input_sqs_queue_arn
    local distribution_sns_topic_arn
    local schedulers_group

    prefix="$(get_tf_output_var '.items_core.value.prefix' 'items-infra')"
    common_layer_arn="$(get_tf_output_var '.layer_upload.value.layer_arn' 'common-lambda-layer-upload')"
    plugins_layer_arn="$(get_tf_output_var '.layer_upload.value.layer_arn' 'plugins-lambda-layer-upload')"
    lambda_zip_path="$(readlink -f "${DEPLOY_DIR}/schedulers-lambda.zip")"
    input_sqs_queue_arn="$(get_tf_output_var '.items_core.value.output_sqs_arn' 'items-infra')"
    distribution_sns_topic_arn="$(get_tf_output_var '.distribution_sns.value.sns_topic_arn' 'distribution-sns')"
    schedulers_group="$(get_tf_output_var '.items_core.value.prefix' 'items-infra')"
    echo "-var prefix=${prefix} -var common_layer_arn=${common_layer_arn} -var plugins_layer_arn=${plugins_layer_arn} -var lambda_zip_path=${lambda_zip_path} -var input_sqs_queue_arn=${input_sqs_queue_arn} -var distribution_sns_topic_arn=${distribution_sns_topic_arn} -var schedulers_group=${schedulers_group}"
}

function schedulers-lambdas-upload-pre-deploy-terraform() {
    schedulers-lambdas-upload-common
}

function schedulers-lambdas-upload-pre-destroy-terraform() {
    schedulers-lambdas-upload-common
}

function distribution-sns-common() {
    local prefix
    prefix="$(get_tf_output_var '.items_core.value.prefix' 'items-infra')"
    echo "-var prefix=${prefix}"
}

function distribution-sns-pre-deploy-terraform() {
    distribution-sns-common
}

function distribution-sns-pre-destroy-terraform() {
    distribution-sns-common
}

function items-infra-common() {
    :
}

function items-infra-pre-deploy-terraform() {
    items-infra-common
}


function items-infra-pre-destroy-terraform() {
    items-infra-common
}

function items-front-upload-common() {
    local bucket_name
    local build_dir_path
    bucket_name="$(get_tf_output_var '.items_core.value.front_bucket_id' 'items-infra')"
    build_dir_path="${DEPLOY_DIR}/front"

    echo "-var front_bucket_name=${bucket_name} -var build_dir_path=${build_dir_path}"
}

function items-front-upload-pre-deploy-terraform() {
    local client_pool_id

    client_pool_id="$(get_tf_output_var '.items_core.value.cognito_user_pool_client_id' 'items-infra')"
    if [ -z "${client_pool_id}" ]; then
        echo "ERROR: Couldn't get UserPoolClientId from TF outputs!"
        exit 1
    fi

    echoerr "Updating front/build/.env with new values"
    sed -i "s/CLIENT_POOL_ID: \".*\"/CLIENT_POOL_ID: \"${client_pool_id}\"/" "${DEPLOY_DIR}/front/env-config.js"

    items-front-upload-common
}

function items-front-upload-pre-destroy-terraform() {
    items-front-upload-common
}


function items-lambdas-upload-common() {
    local prefix
    local api_id
    local api_authorizer_id
    local common_layer_arn
    local plugins_layer_arn
    local lambda_zip_path
    local dynamodb_name
    local dynamodb_stream_arn
    local output_sqs_arn
    local output_sqs_url
    prefix="$(get_tf_output_var '.items_core.value.prefix' 'items-infra')"
    api_id="$(get_tf_output_var '.items_core.value.api_gateway_id' 'items-infra')"
    api_execution_arn="$(get_tf_output_var '.items_core.value.api_gateway_execution_arn' 'items-infra')"
    api_authorizer_id="$(get_tf_output_var '.items_core.value.cognito_authorizer_id' 'items-infra')"
    common_layer_arn="$(get_tf_output_var '.layer_upload.value.layer_arn' 'common-lambda-layer-upload')"
    plugins_layer_arn="$(get_tf_output_var '.layer_upload.value.layer_arn' 'plugins-lambda-layer-upload')"
    lambda_zip_path="$(readlink -f "${DEPLOY_DIR}/items-lambda.zip")"
    dynamodb_stream_arn="$(get_tf_output_var '.items_core.value.items_dynamodb_stream_arn' 'items-infra')"
    output_sqs_arn="$(get_tf_output_var '.items_core.value.output_sqs_arn' 'items-infra')"
    output_sqs_url="$(get_tf_output_var '.items_core.value.output_sqs_url' 'items-infra')"

    dynamodb_name="$(get_tf_output_var '.items_core.value.items_dynamodb_name' 'items-infra')"

    echo "-var prefix=${prefix} -var api_id=${api_id} -var api_execution_arn=${api_execution_arn} -var api_authorizer_id=${api_authorizer_id} -var common_layer_arn=${common_layer_arn} -var plugins_layer_arn=${plugins_layer_arn} -var lambda_zip_path=${lambda_zip_path} -var dynamodb_name=${dynamodb_name} -var dynamodb_stream_arn=${dynamodb_stream_arn} -var output_sqs_arn=${output_sqs_arn} -var output_sqs_url=${output_sqs_url}"
}

function items-lambdas-upload-pre-deploy-terraform() {
    items-lambdas-upload-common
}

function items-lambdas-upload-pre-destroy-terraform() {
    items-lambdas-upload-common
}
