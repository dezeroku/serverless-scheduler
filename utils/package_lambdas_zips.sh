#!/usr/bin/env bash

set -euo pipefail

RUNDIR="$(readlink -f "$(dirname "$0")")"
pushd "${RUNDIR}/.."

# shellcheck source=utils/libs/common.sh
. "${RUNDIR}/libs/common.sh"

function package_service() {
    local service
    service="${1}"
    ./"${service}/bin/package_lambda_entrypoint"

    service_zip_name=$(sanitize_plugin_name "${service}")
    cp "./${service}/.packaging/result/lambda.zip" "${DEPLOY_DIR}/${service_zip_name}-lambda.zip"
}

[ -z "${1:-}" ] && echo "You need to provide service name" && exit 1

BUILD_TARGET="${1}"

package_service "${BUILD_TARGET}"
