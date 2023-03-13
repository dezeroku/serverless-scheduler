#!/usr/bin/env bash

set -euo pipefail

# Start in root of the repo
RUNDIR="$(readlink -f "$(dirname "$0")")"
cd "${RUNDIR}"

# shellcheck source=utils/libs/common.sh
. "${RUNDIR}/libs/common.sh"

# shellcheck source=utils/deploy_lib.sh
. "${RUNDIR}/libs/deploy_lib.sh"

[ -z "${DEPLOY_ENV:-}" ] && DEPLOY_ENV="dev"

for x in $(echo "${DEPLOYABLE_TARGETS}" | tr ' ' '\n' | tac); do
    if [[ "${DEPLOY_ENV}" == "auto" ]]; then
        contains "${AVAILABLE_PLUGINS}" "${x}" && echo "Skipping ${x}, as it's the 'auto' deployment" && continue
    fi

    ./teardown.sh "${x}"
done
