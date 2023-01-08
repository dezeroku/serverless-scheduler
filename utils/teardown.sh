#!/usr/bin/env bash

set -euo pipefail

# Start in root of the repo
RUNDIR="$(readlink -f "$(dirname "$0")")"
cd "${RUNDIR}/.."


# TODO: remove content from front bucket

serverless remove

pushd terraform
terraform destroy
popd

rm -rf .deployment-temp
