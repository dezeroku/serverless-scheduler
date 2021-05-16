#!/usr/bin/env bash

# Apply additional operations that have to be done before
# the chart can be packaged

set -e

if [ -z "${GIT_HASH}" ]; then
    echo "Trying to read git hash from the repo"
    GIT_HASH="$(git rev-parse HEAD)"
fi

echo "The GIT_HASH to be used is: ${GIT_HASH}"

sed "s/%%SHA-SPECIAL-TOKEN%%/${GIT_HASH}/" Chart.tpl > Chart.yaml
