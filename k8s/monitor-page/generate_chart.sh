#!/usr/bin/env bash

# Apply additional operations that have to be done before
# the chart can be packaged

set -e

if [ -z "${MONITOR_CHART_GIT_HASH}" ]; then
    echo "Trying to read git hash from the repo"
    MONITOR_CHART_GIT_HASH="$(git rev-parse HEAD)"
fi

echo "The MONITOR_CHART_GIT_HASH to be used is: ${MONITOR_CHART_GIT_HASH}"

sed "s/%%SHA-SPECIAL-TOKEN%%/${MONITOR_CHART_GIT_HASH}/" Chart.tpl > Chart.yaml
