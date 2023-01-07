#!/usr/bin/env bash

set -euo pipefail

# Start in root of the repo
RUNDIR="$(readlink -f "$(dirname "$0")")"
cd "${RUNDIR}/.."


serverless remove

sls delete_domain

serverless remove-cert

cd terraform

tf destroy
