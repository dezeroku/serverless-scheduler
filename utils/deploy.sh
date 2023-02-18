#!/usr/bin/env bash

set -euxo pipefail

# Start in root of the repo
RUNDIR="$(readlink -f "$(dirname "$0")")"
cd "${RUNDIR}/.."

# shellcheck source=utils/deploy_lib.sh
. "${RUNDIR}/deploy_lib.sh"

[ -z "${1:-}" ] && usage
[ -z "${DEPLOY_ENV:-}" ] && DEPLOY_ENV="dev"

DEPLOY_TARGET="${1}"
contains "${DEPLOYABLE_TARGETS} API" "${DEPLOY_TARGET}" || usage

# TODO: convert this to terraform deployment like the rest
if [[ "${DEPLOY_TARGET}" == "API" ]]; then
    echo "Starting SLS deployment"
    pushd serverless
    DEPLOY_ENV="${DEPLOY_ENV}" serverless deploy
    popd
    exit 0
fi

deploy_terraform "${DEPLOY_TARGET}"
