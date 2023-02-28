#!/usr/bin/env bash
# This is a library that's meant to be sourced
#
function echoerr() {
    echo "$@" 1>&2
}

function contains() {
    [[ " $1 " =~ .*\ $2\ .* ]] && return 0 || return 1
}

DEPLOY_DIR="$(readlink -f "${RUNDIR}/../.deployment-temp/build")"
export DEPLOY_DIR
