#!/usr/bin/env bash

set -euo pipefail

# Start in root of the repo
RUNDIR="$(readlink -f "$(dirname "$0")")"
cd "${RUNDIR}"

# shellcheck source=utils/libs/common.sh
. "${RUNDIR}/libs/common.sh"

pushd ".."
rm -rf "${DEPLOY_DIR}"
mkdir -p "${DEPLOY_DIR}"
popd

for x in ${BUILD_TARGETS}; do
    ./build.sh "${x}"
done
