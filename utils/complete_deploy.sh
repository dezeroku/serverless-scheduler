#!/usr/bin/env bash

set -euo pipefail

# Start in root of the repo
RUNDIR="$(readlink -f "$(dirname "$0")")"
cd "${RUNDIR}"

./deploy.sh items-infra
./deploy.sh common-lambda-layer-upload
./deploy.sh items-lambdas-upload
./deploy.sh items-front-upload
./deploy.sh distribution-sns
./deploy.sh schedulers-lambdas-upload
