#!/usr/bin/env bash

set -euo pipefail

# Start in root of the repo
RUNDIR="$(readlink -f "$(dirname "$0")")"
cd "${RUNDIR}/.."

# shellcheck source=utils/libs/common.sh
. "${RUNDIR}/libs/common.sh"

[ -z "${DEPLOY_ENV:-}" ] && DEPLOY_ENV="dev"

pushd terraform/deployments
#if [[ "${DEPLOY_ENV}" == "auto" ]]; then
#    contains "${AVAILABLE_PLUGINS}" "${x}" && echo "Skipping ${x}, as it's the 'auto' deployment" && continue
#fi
terragrunt run-all apply --terragrunt-working-dir ${DEPLOY_ENV}
