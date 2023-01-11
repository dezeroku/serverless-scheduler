#!/usr/bin/env bash

set -euo pipefail

function get_front_vars() {
    echo "Obtaining requires variables from TF"
    echo "Make sure that TF deployment was run first"
    CLIENT_POOL_ID="$(jq -r '.cognito_user_pool_client_id.value' < .deployment-temp/terraform/outputs.json)"
    if [ -z "${CLIENT_POOL_ID}" ]; then
        echo "ERROR: Couldn't get UserPoolClientId from TF outputs!"
        exit 1
    fi
}

function set_front_vars() {
    get_front_vars
    pushd front

    echo "Updating front/.env with new values"
    sed -i "s/CLIENT_POOL_ID=.*/CLIENT_POOL_ID=${CLIENT_POOL_ID}/" .env

    echo "Regenerating front/env-config.js"
    ./env.sh

    popd
}

function build_front() {
    set_front_vars
    ## Build the actual static front delivery
    pushd ./front
    echo "Starting front build"
    make build
    popd
}

function upload_front() {
    local bucket_name
    bucket_name="$(jq -r '.front_bucket_id.value' < .deployment-temp/terraform/outputs.json)"

    if [ -z "${bucket_name}" ]; then
        echo "Couldn't read bucket name from TF outputs!"
        exit 1
    fi

    pushd terraform/front

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
HEREDOC

    exit 1
}

function provision_terraform_core() {
    pushd terraform/core/

    suffix="-var-file=../global.tfvars.json"

    if [ -f "secret-values.tfvars" ]; then
        suffix="${suffix} -var-file=secret-values.tfvars"
    fi

    # shellcheck disable=SC2086 # Intended globbing
    terraform apply ${suffix}

    mkdir -p ../../.deployment-temp/terraform
    terraform output -json > ../../.deployment-temp/terraform/outputs.json

    popd
}

[ -z "${1:-}" ] && usage

# Start in root of the repo
RUNDIR="$(readlink -f "$(dirname "$0")")"
cd "${RUNDIR}/.."

BUILD_INFRA=false
BUILD_API=false
BUILD_FRONT=false

[ -z "${PACKAGE_LAMBDAS:-}" ] && PACKAGE_LAMBDAS="true"

[[ "$1" == "INFRA" ]] && BUILD_INFRA=true
[[ "$1" == "API" ]] && BUILD_API=true
[[ "$1" == "FRONT" ]] && BUILD_FRONT=true
[[ "$1" == "FULL" ]] && BUILD_INFRA=true && BUILD_API=true && BUILD_FRONT=true

if [[ "${BUILD_INFRA}" == "true" ]]; then
    echo "Provisioning terraform infra"
    provision_terraform_core
fi

if [[ "${BUILD_API}" == "true" ]]; then
    if [[ "${PACKAGE_LAMBDAS}" == "true" ]]; then
        echo "Packaging Lambdas"
        "${RUNDIR}"/package_lambdas_zips.sh
    fi

    echo "Starting SLS deployment"
    serverless deploy
fi

# Front is built last, as we need to push values from TF deployment into it
if [[ "$BUILD_FRONT" == "true" ]]; then
    if [[ "${BUILD_INFRA}" == "false" ]]; then
        # make sure that proper TF outputs are in place
        provision_terraform_core
    fi

    build_front
    upload_front
fi
