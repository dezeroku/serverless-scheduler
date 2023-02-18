#!/usr/bin/env bash
# This is a library that's meant to be sourced

function items-front-upload-pre-deploy-terraform() {
    local client_pool_id
    client_pool_id="$(jq -r '.items_core.value.cognito_user_pool_client_id' < "${RUNDIR}/../.deployment-temp/${DEPLOY_ENV}/terraform/items-infra-outputs.json")"
    if [ -z "${client_pool_id}" ]; then
        echo "ERROR: Couldn't get UserPoolClientId from TF outputs!"
        exit 1
    fi

    echoerr "Updating front/build/.env with new values"
    sed -i "s/CLIENT_POOL_ID: \".*\"/CLIENT_POOL_ID: \"${client_pool_id}\"/" "${RUNDIR}/../front/build/env-config.js"

    local bucket_name
    bucket_name="$(jq -r '.items_core.value.front_bucket_id' < "${RUNDIR}/../.deployment-temp/${DEPLOY_ENV}/terraform/items-infra-outputs.json")"

    echo "-var front_bucket_name=${bucket_name}"
}

function items-front-upload-pre-destroy-terraform() {
    local bucket_name
    bucket_name="$(jq -r '.items_core.value.front_bucket_id' < "${RUNDIR}/../.deployment-temp/${DEPLOY_ENV}/terraform/items-infra-outputs.json")"

    echo "-var front_bucket_name=${bucket_name}"
}


function items-lambdas-upload-common() {
    local prefix
    local api_id
    local api_authorizer_id
    local lambda_zip_path
    local dynamodb_name
    prefix="$(jq -r '.items_core.value.prefix' < "${RUNDIR}/../.deployment-temp/${DEPLOY_ENV}/terraform/items-infra-outputs.json")"
    api_id="$(jq -r '.items_core.value.api_gateway_id' < "${RUNDIR}/../.deployment-temp/${DEPLOY_ENV}/terraform/items-infra-outputs.json")"
    api_execution_arn="$(jq -r '.items_core.value.api_gateway_execution_arn' < "${RUNDIR}/../.deployment-temp/${DEPLOY_ENV}/terraform/items-infra-outputs.json")"
    api_authorizer_id="$(jq -r '.items_core.value.cognito_authorizer_id' < "${RUNDIR}/../.deployment-temp/${DEPLOY_ENV}/terraform/items-infra-outputs.json")"
    lambda_zip_path="$(readlink -f "${RUNDIR}/../.deployment-temp/lambda-zips/items-lambda.zip")"
    dynamodb_name="$(jq -r '.items_core.value.items_dynamodb_name' < "${RUNDIR}/../.deployment-temp/${DEPLOY_ENV}/terraform/items-infra-outputs.json")"

    echo "-var prefix=${prefix} -var api_id=${api_id} -var api_execution_arn=${api_execution_arn} -var api_authorizer_id=${api_authorizer_id} -var lambda_zip_path=${lambda_zip_path} -var dynamodb_name=${dynamodb_name}"
}

function items-lambdas-upload-pre-deploy-terraform() {
    items-lambdas-upload-common
}

function items-lambdas-upload-pre-destroy-terraform() {
    items-lambdas-upload-common
}
