#!/usr/bin/env bash

set -euo pipefail

# Start in root of the repo
RUNDIR="$(readlink -f "$(dirname "$0")")"
cd "${RUNDIR}/.."


serverless remove

pushd terraform
tf destroy
popd

rm -rf .deployment-temp
