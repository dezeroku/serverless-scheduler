#!/usr/bin/env bash

set -euo pipefail

function build_items_front() {
    ## Build the actual static front delivery
    pushd ./front
    echo "Starting front build"
    ./build.sh
    echo "Copying files to ${DEPLOY_DIR}/front"
    mkdir -p "${DEPLOY_DIR}/front"
    cp -r ./.packaging/result/* "${DEPLOY_DIR}/front"
    popd
}

function usage() {
    cat << HEREDOC
build.sh SCOPE
where SCOPE can be one of:
$(echo "${BUILD_TARGETS}" | tr ' ' '\n' | sed -e 's/^/- /')
HEREDOC

    exit 1
}

# Start in root of the repo
RUNDIR="$(readlink -f "$(dirname "$0")")"
cd "${RUNDIR}/.."

# shellcheck source=utils/libs/common.sh
. "${RUNDIR}/libs/common.sh"

[ -z "${1:-}" ] && usage
BUILD_TARGET="${1}"

contains "${BUILD_TARGETS}" "${BUILD_TARGET}" || usage

# This is specifically for CI use
if [[ "${GHA_DOCKER_CACHING:-false}" == "true" ]]; then
    export GHA_DOCKER_CACHING="true"
else
    export GHA_DOCKER_CACHING="false"
fi

if [[ "${BUILD_TARGET}" == "items-front" ]]; then
    build_items_front
else
    "${RUNDIR}"/package_lambdas_zips.sh "${BUILD_TARGET}"
fi
