#!/usr/bin/env bash
# This is a library that's meant to be sourced
#
function echoerr() {
    echo "$@" 1>&2
}

function contains() {
    [[ " $1 " =~ .*\ $2\ .* ]] && return 0 || return 1
}

DEPLOY_DIR="${RUNDIR}/../.deployment-temp/build"
mkdir -p "${DEPLOY_DIR}"
DEPLOY_DIR="$(readlink -f "${DEPLOY_DIR}")"
export DEPLOY_DIR
