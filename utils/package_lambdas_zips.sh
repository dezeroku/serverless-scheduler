#!/usr/bin/env bash

RUNDIR="$(readlink -f "$(dirname "$0")")"

set -euo pipefail

pushd "${RUNDIR}/.."

# Prepare dir
DEPLOY_DIR="lambda-deployment-zips"
rm -rf "${DEPLOY_DIR}"
mkdir "${DEPLOY_DIR}"

function package_service() {
    local service
    service="${1}"
    ./"${service}/bin/package_lambda_entrypoint"

    cp "./${service}/.packaging/result/lambda.zip" "${DEPLOY_DIR}/${service}-lambda.zip"
}

# Package services
package_service items
package_service schedulers
