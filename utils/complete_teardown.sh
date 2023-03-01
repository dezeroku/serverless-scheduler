#!/usr/bin/env bash

set -euo pipefail

# Start in root of the repo
RUNDIR="$(readlink -f "$(dirname "$0")")"
cd "${RUNDIR}"

./teardown.sh schedulers-lambdas-upload
./teardown.sh distribution-sns
./teardown.sh items-front-upload
./teardown.sh items-lambdas-upload
./teardown.sh common-lambda-layer-upload
./teardown.sh items-infra
