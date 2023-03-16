#!/usr/bin/env bash

set -euo pipefail

# Start in root of the repo
RUNDIR="$(readlink -f "$(dirname "$0")")"
cd "${RUNDIR}/.."

# shellcheck source=utils/deploy_lib.sh
. "${RUNDIR}/libs/deploy_lib.sh"

[ -z "${1:-}" ] && usage
[ -z "${DEPLOY_ENV:-}" ] && DEPLOY_ENV="dev"

DESTROY_TARGET="${1}"
contains "${DEPLOYABLE_TARGETS}" "${DESTROY_TARGET}" || usage

pushd terraform/deployments/"${DEPLOY_ENV}/${DESTROY_TARGET}"
terragrunt destroy
