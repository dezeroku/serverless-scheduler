#!/usr/bin/env bash

set -euo pipefail

function get_front_vars() {
    echo "Obtaining requires variables from SLS"
    echo "Make sure that SLS deployment was run first"
    CLIENT_POOL_ID="$(sls info --verbose | grep "UserPoolClientId" | cut -d ":" -f2 | xargs)"
    if [ -z "${CLIENT_POOL_ID}" ]; then
        echo "ERROR: Couldn't get UserPoolClientId from sls info!"
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
    sls s3sync
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

function provision_terraform() {
    pushd terraform

    if [ -f "secret-values.tfvars" ]; then
        terraform apply -var-file="secret-values.tfvars"
    else
        terraform apply
    fi

    mkdir -p ../.deployment-temp/terraform
    terraform output -json > ../.deployment-temp/terraform/outputs.json

    popd
}

[ -z "${1:-}" ] && usage

# Start in root of the repo
RUNDIR="$(readlink -f "$(dirname "$0")")"
cd "${RUNDIR}/.."

BUILD_INFRA=false
BUILD_API=false
BUILD_FRONT=false

[[ "$1" == "INFRA" ]] && BUILD_INFRA=true
[[ "$1" == "API" ]] && BUILD_API=true
[[ "$1" == "FRONT" ]] && BUILD_FRONT=true
[[ "$1" == "FULL" ]] && BUILD_INFRA=true && BUILD_API=true && BUILD_FRONT=true

if [[ "${BUILD_INFRA}" == "true" ]]; then
    echo "Provisioning terraform infra"
    provision_terraform

    echo "Creating certs"
    serverless create-cert

    echo "Creating domain"
    sls create_domain
fi

if [[ "${BUILD_API}" == "true" ]]; then
    echo "Packaging Lambdas"
    "${RUNDIR}"/package_lambdas_zips.sh

    echo "Starting SLS deployment"
    serverless deploy --nos3sync
fi

# Front is built last, as we need to push values from SLS deployment into it

if [[ "$BUILD_FRONT" == "true" ]]; then
    build_front
    upload_front
fi
