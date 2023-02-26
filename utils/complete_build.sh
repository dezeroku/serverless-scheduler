#!/usr/bin/env bash

set -euo pipefail

# Start in root of the repo
RUNDIR="$(readlink -f "$(dirname "$0")")"
cd "${RUNDIR}"

pushd ".."
DEPLOY_DIR=".deployment-temp/lambda-zips"
rm -rf "${DEPLOY_DIR}"
popd

./build.sh items
./build.sh items-front
./build.sh schedulers
