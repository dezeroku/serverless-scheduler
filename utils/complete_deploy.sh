#!/usr/bin/env bash

set -euo pipefail

# Start in root of the repo
RUNDIR="$(readlink -f "$(dirname "$0")")"
cd "${RUNDIR}"

# shellcheck source=utils/libs/common.sh
. "${RUNDIR}/libs/common.sh"

# shellcheck source=utils/deploy_lib.sh
. "${RUNDIR}/libs/deploy_lib.sh"

for x in ${DEPLOYABLE_TARGETS}; do
    ./deploy.sh "${x}"
done
