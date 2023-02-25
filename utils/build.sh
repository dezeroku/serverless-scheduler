#!/usr/bin/env bash

set -euo pipefail

function build_front() {
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
- items
- front
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

contains "items front" "${BUILD_TARGET}" || usage

if [[ "${BUILD_TARGET}" == "items" ]]; then
    "${RUNDIR}"/package_lambdas_zips.sh "items"
elif [[ "${BUILD_TARGET}" == "front" ]]; then
    build_front
fi
