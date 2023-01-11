#!/usr/bin/env bash

set -euo pipefail

# Start in root of the repo
RUNDIR="$(readlink -f "$(dirname "$0")")"
cd "${RUNDIR}/.."

function destroy_terraform_core() {
    pushd terraform/core

    suffix="-var-file=../global.tfvars.json"

    if [ -f "secret-values.tfvars" ]; then
        suffix="${suffix} -var-file=secret-values.tfvars"
    fi

    # shellcheck disable=SC2086 # Intended globbing
    terraform destroy ${suffix}

    popd
}

serverless remove

destroy_terraform_core

rm -rf .deployment-temp
