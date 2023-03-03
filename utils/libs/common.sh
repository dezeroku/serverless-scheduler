#!/usr/bin/env bash
# This is a library that's meant to be sourced
#
function echoerr() {
    echo "$@" 1>&2
}

function contains() {
    [[ " $1 " =~ .*\ $2\ .* ]] && return 0 || return 1
}

function sanitize_plugin_name() {
    local service="${1}"
    echo "${service}" | tr '/' '-'
}

CORE_TARGETS="common items items-front schedulers plugins-interface"
PLUGINS_DIR="${RUNDIR}/../plugins"
AVAILABLE_PLUGINS="$(find "${PLUGINS_DIR}" -mindepth 1 -maxdepth 1 -type d | sed "s#${RUNDIR}/../##" | tr '\n' ' ' | head -c -1)"

BUILD_TARGETS="${CORE_TARGETS} ${AVAILABLE_PLUGINS}"
export CORE_TARGETS
export AVAILABLE_PLUGINS
export BUILD_TARGETS

DEPLOY_DIR="${RUNDIR}/../.deployment-temp/build"
mkdir -p "${DEPLOY_DIR}"
DEPLOY_DIR="$(readlink -f "${DEPLOY_DIR}")"
export DEPLOY_DIR
