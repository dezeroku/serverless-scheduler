#!/usr/bin/env bash

set -e

function build_front() {
    ## Build the actual static front delivery
    pushd ../../front
    make build
    popd
}

[[ -n "$1" ]] && [[ "$1" == "build_front" ]] && build_front

serverless create-cert

sls create_domain

serverless deploy
