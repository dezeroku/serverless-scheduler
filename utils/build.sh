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
- FULL
- API
- FRONT
HEREDOC

    exit 1
}

[ -z "${1:-}" ] && usage

# Start in root of the repo
RUNDIR="$(readlink -f "$(dirname "$0")")"
cd "${RUNDIR}/.."

BUILD_API=false
BUILD_FRONT=false

[[ "$1" == "API" ]] && BUILD_API=true
[[ "$1" == "FRONT" ]] && BUILD_FRONT=true
[[ "$1" == "FULL" ]] && BUILD_API=true && BUILD_FRONT=true

if [[ "${BUILD_API}" == "true" ]]; then
    echo "Packaging Lambdas"
    "${RUNDIR}"/package_lambdas_zips.sh
fi

if [[ "$BUILD_FRONT" == "true" ]]; then
    build_front
fi
