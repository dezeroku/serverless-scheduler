#!/usr/bin/env bash

set -euo pipefail

# Start in root of the repo
RUNDIR="$(readlink -f "$(dirname "$0")")"
cd "${RUNDIR}/.."

# shellcheck source=utils/deploy_lib.sh
. "${RUNDIR}/deploy_lib.sh"

[ -z "${1:-}" ] && usage
[ -z "${DEPLOY_ENV:-}" ] && DEPLOY_ENV="dev"

DESTROY_TARGET="${1}"
contains "${DEPLOYABLE_TARGETS} API" "${DESTROY_TARGET}" || usage

# TODO: convert this to terraform deployment like the rest
if [[ "${DESTROY_TARGET}" == "API" ]]; then
    echo "Starting SLS deployment"
    pushd serverless
    DEPLOY_ENV="${DEPLOY_ENV}" serverless remove
    popd
    exit 0
fi

destroy_terraform "${DESTROY_TARGET}"
rm -rf ".deployment-temp/${DEPLOY_ENV}/terraform/${DESTROY_TARGET}-outputs.json"
