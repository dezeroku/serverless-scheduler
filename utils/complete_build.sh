#!/usr/bin/env bash

set -euo pipefail

# Start in root of the repo
RUNDIR="$(readlink -f "$(dirname "$0")")"
cd "${RUNDIR}"

# shellcheck source=utils/libs/common.sh
. "${RUNDIR}/libs/common.sh"

pushd ".."
rm -rf "${DEPLOY_DIR}"
popd

./build.sh common
./build.sh items
./build.sh items-front
./build.sh schedulers
