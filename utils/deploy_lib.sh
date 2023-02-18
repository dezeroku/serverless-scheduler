#!/usr/bin/env bash
# This is a library that's meant to be sourced
# This is all assumed to be running from the root of repository
# RUNDIR is assumed to point to this directory
DEPLOYMENTS_DIR="./terraform/deployments"
# Find deployable targets, convert newlines to spaces, remove last space
DEPLOYABLE_TARGETS="$(find "${DEPLOYMENTS_DIR}" -mindepth 1 -maxdepth 1 -type d | awk -F'/' '{print $(NF)}' | tr '\n' ' ' | head -c -1)"

# shellcheck source=utils/deploy_lib_hooks.sh
. "${RUNDIR}/deploy_lib_hooks.sh"

function echoerr() {
    echo "$@" 1>&2
}

function contains() {
    [[ " $1 " =~ .*\ $2\ .* ]] && return 0 || return 1
}

function deploy_terraform() {
    local deploy_target="${1}"
    pushd "${DEPLOYMENTS_DIR}/${deploy_target}" || exit 1

    terraform workspace select "${DEPLOY_ENV}"
    suffix="-var-file=../global.tfvars.json"

    if [ -f "${DEPLOY_ENV}.tfvars.json" ]; then
        suffix="${suffix} -var-file=${DEPLOY_ENV}.tfvars.json"
    fi

    if [ -f "${DEPLOY_ENV}-secret-values.tfvars" ]; then
        suffix="${suffix} -var-file=${DEPLOY_ENV}-secret-values.tfvars"
    fi

    if [[ "$(type -t "${deploy_target}-pre-deploy-terraform")" == function ]]; then
        echo "Running pre-deploy-terraform for ${deploy_target}"
        suffix="${suffix} $("${deploy_target}-pre-deploy-terraform")"
    fi

    # shellcheck disable=SC2086 # Intended globbing
    terraform apply ${suffix}

    mkdir -p "${RUNDIR}/../.deployment-temp/${DEPLOY_ENV}/terraform"
    terraform output -json > "../../../.deployment-temp/${DEPLOY_ENV}/terraform/${deploy_target}-outputs.json"

    popd || exit 1
}

function destroy_terraform() {
    local destroy_target="${1}"
    pushd "${DEPLOYMENTS_DIR}/${destroy_target}" || exit 1

    terraform workspace select "${DEPLOY_ENV}"
    suffix="-var-file=../global.tfvars.json"

    if [ -f "${DEPLOY_ENV}.tfvars.json" ]; then
        suffix="${suffix} -var-file=${DEPLOY_ENV}.tfvars.json"
    fi

    if [ -f "${DEPLOY_ENV}-secret-values.tfvars" ]; then
        suffix="${suffix} -var-file=${DEPLOY_ENV}-secret-values.tfvars"
    fi

    if [[ "$(type -t "${destroy_target}-pre-destroy-terraform")" == function ]]; then
        echo "Running pre-destroy-terraform for ${destroy_target}"
        suffix="${suffix} $("${destroy_target}-pre-destroy-terraform")"
    fi

    # shellcheck disable=SC2086 # Intended globbing
    terraform destroy ${suffix}

    popd || exit 1
}

function usage() {
    cat << HEREDOC
$0 SCOPE
where SCOPE can be one of:
- API
$(echo "${DEPLOYABLE_TARGETS}" | tr ' ' '\n' | sed -e 's/^/- /')

You can also pass DEPLOY_ENV env variable to choose
to which env changes should be applied
HEREDOC

    exit 1
}
