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
