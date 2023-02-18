#!/usr/bin/env bash

RUNDIR="$(readlink -f "$(dirname "$0")")"

set -euo pipefail

pushd "${RUNDIR}/.."

# Prepare dir
DEPLOY_DIR=".deployment-temp/lambda-zips"
rm -rf "${DEPLOY_DIR}"
mkdir -p "${DEPLOY_DIR}"

function package_service() {
    local service
    service="${1}"
    ./"${service}/bin/package_lambda_entrypoint"

    cp "./${service}/.packaging/result/lambda.zip" "${DEPLOY_DIR}/${service}-lambda.zip"
}

[ -z "${1:-}" ] && echo "You need to provide service name" && exit 1

BUILD_TARGET="${1}"

package_service "${BUILD_TARGET}"
