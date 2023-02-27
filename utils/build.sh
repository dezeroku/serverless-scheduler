#!/usr/bin/env bash

set -euo pipefail

function build_items_front() {
    ## Build the actual static front delivery
    pushd ./front
    echo "Starting front build"
    make build
    popd
}

function usage() {
    cat << HEREDOC
deploy.sh SCOPE
where SCOPE can be one of:
- common
- items
- schedulers
- items-front
HEREDOC

    exit 1
}

[ -z "${1:-}" ] && usage
BUILD_TARGET="${1}"

# Start in root of the repo
RUNDIR="$(readlink -f "$(dirname "$0")")"
cd "${RUNDIR}/.."

# shellcheck source=utils/libs/common.sh
. "${RUNDIR}/libs/common.sh"

contains "common items items-front schedulers" "${BUILD_TARGET}" || usage

if [[ "${BUILD_TARGET}" == "common" ]]; then
    "${RUNDIR}"/package_lambdas_zips.sh "common"
elif [[ "${BUILD_TARGET}" == "items" ]]; then
    "${RUNDIR}"/package_lambdas_zips.sh "items"
elif [[ "${BUILD_TARGET}" == "schedulers" ]]; then
    "${RUNDIR}"/package_lambdas_zips.sh "schedulers"
elif [[ "${BUILD_TARGET}" == "items-front" ]]; then
    build_items_front
fi
