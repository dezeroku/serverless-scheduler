#!/usr/bin/env bash

set -euo pipefail

# Start in root of the repo
RUNDIR="$(readlink -f "$(dirname "$0")")"
cd "${RUNDIR}/.."

function destroy_terraform_core() {
    pushd "terraform/deployments/items-infra"
    terraform workspace select "${DEPLOY_ENV}"

    suffix="-var-file=../global.tfvars.json"

    if [ -f "${DEPLOY_ENV}.tfvars.json" ]; then
        suffix="${suffix} -var-file=${DEPLOY_ENV}.tfvars.json"
    fi

    if [ -f "${DEPLOY_ENV}-secret-values.tfvars" ]; then
        suffix="${suffix} -var-file=${DEPLOY_ENV}-secret-values.tfvars"
    fi

    # shellcheck disable=SC2086 # Intended globbing
    terraform destroy ${suffix}

    popd
}

[ -z "${DEPLOY_ENV:-}" ] && DEPLOY_ENV="dev"

pushd serverless
DEPLOY_ENV="${DEPLOY_ENV}" serverless remove
popd

destroy_terraform_core

rm -rf ".deployment-temp/${DEPLOY_ENV}"
