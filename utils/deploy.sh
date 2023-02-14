#!/usr/bin/env bash

set -euo pipefail

function get_front_vars() {
    echo "Obtaining requires variables from TF"
    echo "Make sure that TF deployment was run first"
    CLIENT_POOL_ID="$(jq -r '.core.value.cognito_user_pool_client_id' < ".deployment-temp/${DEPLOY_ENV}/terraform/outputs.json")"
    if [ -z "${CLIENT_POOL_ID}" ]; then
        echo "ERROR: Couldn't get UserPoolClientId from TF outputs!"
        exit 1
    fi
}

function prepare_front_deployment() {
    get_front_vars
    pushd front

    echo "Updating front/build/.env with new values"
    sed -i "s/CLIENT_POOL_ID: \".*\"/CLIENT_POOL_ID: \"${CLIENT_POOL_ID}\"/" build/env-config.js

    popd
}

function upload_front() {
    local bucket_name
    bucket_name="$(jq -r '.core.value.front_bucket_id' < ".deployment-temp/${DEPLOY_ENV}/terraform/outputs.json")"

    if [ -z "${bucket_name}" ]; then
        echo "Couldn't read bucket name from TF outputs!"
        exit 1
    fi

    pushd "terraform/deployments/${DEPLOY_ENV}/front"

    terraform apply -var-file=../global.tfvars.json -var "front_bucket_name=${bucket_name}"

    popd
}

function usage() {
    cat << HEREDOC
deploy.sh SCOPE
where SCOPE can be one of:
- FULL
- API
- FRONT
- INFRA
You can also pass DEPLOY_ENV env variable to choose
to which env changes should be deployed
HEREDOC

    exit 1
}

function provision_terraform_core() {
    pushd "terraform/deployments/${DEPLOY_ENV}/core/"

    suffix="-var-file=../global.tfvars.json"

    if [ -f "secret-values.tfvars" ]; then
        suffix="${suffix} -var-file=secret-values.tfvars"
    fi

    # shellcheck disable=SC2086 # Intended globbing
    terraform apply ${suffix}

    mkdir -p "../../../../.deployment-temp/${DEPLOY_ENV}/terraform"
    terraform output -json > "../../../../.deployment-temp/${DEPLOY_ENV}/terraform/outputs.json"

    popd
}

[ -z "${1:-}" ] && usage



# Start in root of the repo
RUNDIR="$(readlink -f "$(dirname "$0")")"
cd "${RUNDIR}/.."

[ -z "${DEPLOY_ENV:-}" ] && DEPLOY_ENV="dev"

DEPLOY_INFRA=false
DEPLOY_API=false
DEPLOY_FRONT=false

[[ "$1" == "INFRA" ]] && DEPLOY_INFRA=true
[[ "$1" == "API" ]] && DEPLOY_API=true
[[ "$1" == "FRONT" ]] && DEPLOY_FRONT=true
[[ "$1" == "FULL" ]] && DEPLOY_INFRA=true && DEPLOY_API=true && DEPLOY_FRONT=true

if [[ "${DEPLOY_INFRA}" == "true" ]]; then
    echo "Provisioning terraform infra"
    provision_terraform_core
fi

if [[ "${DEPLOY_API}" == "true" ]]; then
    if [[ "${BUILD_API:-false}" == "true" ]]; then
        "${RUNDIR}"/utils/build.sh "API"
    fi

    echo "Starting SLS deployment"
    DEPLOY_ENV="${DEPLOY_ENV}" serverless deploy
fi

# Front is built last, as we need to push values from TF deployment into it
if [[ "$DEPLOY_FRONT" == "true" ]]; then
    if [[ "${BUILD_FRONT:-false}" == "true" ]]; then
        "${RUNDIR}"/utils/build.sh "FRONT"
    fi

    prepare_front_deployment
    upload_front
fi
