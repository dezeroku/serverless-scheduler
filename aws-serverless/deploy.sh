#!/usr/bin/env bash

set -e

# Build the actual static front delivery
pushd ../front
make build
popd

# Deploy files
serverless client deploy --no-confirm
serverless deploy
