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

function schedulers-lambdas-upload-common() {
    local prefix
    local lambda_zip_path
    local input_sqs_queue_url
    local input_sqs_queue_arn
    local distribution_sns_topic_name
    local distribution_sns_topic_arn

    prefix="$(get_tf_output_var '.items_core.value.prefix' 'items-infra')"
    lambda_zip_path="$(readlink -f "${RUNDIR}/../.deployment-temp/lambda-zips/schedulers-lambda.zip")"
    input_sqs_queue_url="$(get_tf_output_var '.items_core.value.output_sqs_url' 'items-infra')"
    input_sqs_queue_arn="$(get_tf_output_var '.items_core.value.output_sqs_arn' 'items-infra')"
    distribution_sns_topic_name="$(get_tf_output_var '.distribution_sns.value.sns_topic_name' 'distribution-sns')"
    distribution_sns_topic_arn="$(get_tf_output_var '.distribution_sns.value.sns_topic_arn' 'distribution-sns')"
    echo "-var prefix=${prefix} -var lambda_zip_path=${lambda_zip_path} -var input_sqs_queue_url=${input_sqs_queue_url} -var input_sqs_queue_arn=${input_sqs_queue_arn} -var distribution_sns_topic_name=${distribution_sns_topic_name} -var distribution_sns_topic_arn=${distribution_sns_topic_arn}"
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

function items-front-upload-pre-deploy-terraform() {
    local client_pool_id

    client_pool_id="$(get_tf_output_var '.items_core.value.cognito_user_pool_client_id' 'items-infra')"
    if [ -z "${client_pool_id}" ]; then
        echo "ERROR: Couldn't get UserPoolClientId from TF outputs!"
        exit 1
    fi

    echoerr "Updating front/build/.env with new values"
    sed -i "s/CLIENT_POOL_ID: \".*\"/CLIENT_POOL_ID: \"${client_pool_id}\"/" "${RUNDIR}/../front/build/env-config.js"

    local bucket_name
    bucket_name="$(get_tf_output_var '.items_core.value.front_bucket_id' 'items-infra')"

    echo "-var front_bucket_name=${bucket_name}"
}

function items-front-upload-pre-destroy-terraform() {
    local bucket_name
    bucket_name="$(get_tf_output_var '.items_core.value.front_bucket_id' 'items-infra')"

    echo "-var front_bucket_name=${bucket_name}"
}


function items-lambdas-upload-common() {
    local prefix
    local api_id
    local api_authorizer_id
    local lambda_zip_path
    local dynamodb_name
    local dynamodb_stream_arn
    local output_sqs_arn
    local output_sqs_url
    prefix="$(get_tf_output_var '.items_core.value.prefix' 'items-infra')"
    api_id="$(get_tf_output_var '.items_core.value.api_gateway_id' 'items-infra')"
    api_execution_arn="$(get_tf_output_var '.items_core.value.api_gateway_execution_arn' 'items-infra')"
    api_authorizer_id="$(get_tf_output_var '.items_core.value.cognito_authorizer_id' 'items-infra')"
    lambda_zip_path="$(readlink -f "${RUNDIR}/../.deployment-temp/lambda-zips/items-lambda.zip")"
    dynamodb_stream_arn="$(get_tf_output_var '.items_core.value.items_dynamodb_stream_arn' 'items-infra')"
    output_sqs_arn="$(get_tf_output_var '.items_core.value.output_sqs_arn' 'items-infra')"
    output_sqs_url="$(get_tf_output_var '.items_core.value.output_sqs_url' 'items-infra')"

    dynamodb_name="$(get_tf_output_var '.items_core.value.items_dynamodb_name' 'items-infra')"

    echo "-var prefix=${prefix} -var api_id=${api_id} -var api_execution_arn=${api_execution_arn} -var api_authorizer_id=${api_authorizer_id} -var lambda_zip_path=${lambda_zip_path} -var dynamodb_name=${dynamodb_name} -var dynamodb_stream_arn=${dynamodb_stream_arn} -var output_sqs_arn=${output_sqs_arn} -var output_sqs_url=${output_sqs_url}"
}

function items-lambdas-upload-pre-deploy-terraform() {
    items-lambdas-upload-common
}

function items-lambdas-upload-pre-destroy-terraform() {
    items-lambdas-upload-common
}
