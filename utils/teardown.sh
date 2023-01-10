#!/usr/bin/env bash

set -euo pipefail

# Start in root of the repo
RUNDIR="$(readlink -f "$(dirname "$0")")"
cd "${RUNDIR}/.."

function destroy_terraform() {
    pushd terraform

    suffix=""

    if [ -f "secret-values.tfvars" ]; then
        suffix="${suffix}-var-file=secret-values.tfvars"
    fi

    terraform destroy ${suffix}

    popd
}

# TODO: remove content from front bucket
serverless remove

destroy_terraform

rm -rf .deployment-temp
