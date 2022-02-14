#!/usr/bin/env bash

set -e

# Build the actual static front delivery
pushd ../front
make build
popd

# Configure domain (the env variable is needed)
[ -z "${apiDomain}" ] && apiDomain=example.com
export apiDomain
sls create_domain

# Deploy files
serverless client deploy --no-confirm

# Deploy an actual app
serverless deploy
