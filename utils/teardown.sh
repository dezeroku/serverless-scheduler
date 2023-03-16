#!/usr/bin/env bash

set -euo pipefail

# Start in root of the repo
RUNDIR="$(readlink -f "$(dirname "$0")")"
cd "${RUNDIR}/.."

[ -z "${1:-}" ] && usage
[ -z "${DEPLOY_ENV:-}" ] && DEPLOY_ENV="dev"

DESTROY_TARGET="${1}"

pushd terraform/deployments/"${DEPLOY_ENV}/${DESTROY_TARGET}"
terragrunt destroy
