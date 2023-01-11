#!/usr/bin/env bash

set -euo pipefail

# Start in root of the repo
RUNDIR="$(readlink -f "$(dirname "$0")")"
cd "${RUNDIR}/.."

function destroy_terraform_core() {
    pushd terraform/core

    suffix=""

    if [ -f "secret-values.tfvars" ]; then
        suffix="${suffix}-var-file=secret-values.tfvars"
    fi

    terraform destroy ${suffix}

    popd
}

serverless remove

destroy_terraform_core

rm -rf .deployment-temp
