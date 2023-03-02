#!/usr/bin/env bash
# This is a library that's meant to be sourced
# This is all assumed to be running from the root of repository
# RUNDIR is assumed to point to this directory

# shellcheck source=utils/libs/common.sh
. "${RUNDIR}/libs/common.sh"

DEPLOYMENTS_DIR="./terraform/deployments"
# Just a hardcoded list to make sure that order is correct for complete_deploy.sh
DEPLOYABLE_TARGETS="items-infra common-lambda-layer-upload items-lambdas-upload items-front-upload distribution-sns schedulers-lambdas-upload ${AVAILABLE_PLUGINS}"

# shellcheck source=utils/libs/deploy_lib_hooks.sh
. "${RUNDIR}/libs/deploy_lib_hooks.sh"


function deploy_terraform() {
    local deploy_target="${1}"
    if [[ "${deploy_target}" =~ plugins/.* ]]; then
        deploy_terraform_impl "$(sanitize_plugin_name "${deploy_target}")" "${PLUGINS_DIR}/${deploy_target#"plugins/"}/terraform" "true"
    else
        deploy_terraform_impl "${deploy_target}" "${DEPLOYMENTS_DIR}/${deploy_target}" "false"
    fi
}

function destroy_terraform() {
    local destroy_target="${1}"
    if [[ "${destroy_target}" =~ plugins/.* ]]; then
        destroy_terraform_impl "$(sanitize_plugin_name "${destroy_target}")" "${PLUGINS_DIR}/${destroy_target#"plugins/"}/terraform" "true"
    else
        destroy_terraform_impl "${destroy_target}" "${DEPLOYMENTS_DIR}/${destroy_target}" "false"
    fi
}

function deploy_terraform_impl() {
    local deploy_target="${1}"
    local deployment_dir="${2}"
    local is_plugin="${3}"

    pushd "${deployment_dir}" || exit 1

    terraform workspace select "${DEPLOY_ENV}"
    if [[ "${is_plugin}" == "false" ]]; then
        suffix="-var-file=../global.tfvars.json"
    else
        suffix=""
    fi

    if [ -f "${DEPLOY_ENV}.tfvars.json" ]; then
        suffix="${suffix} -var-file=${DEPLOY_ENV}.tfvars.json"
    fi

    if [ -f "${DEPLOY_ENV}-secret-values.tfvars" ]; then
        suffix="${suffix} -var-file=${DEPLOY_ENV}-secret-values.tfvars"
    fi

    if [[ "${is_plugin}" == "true" ]]; then
        echo "Running plugin-terraform-common for ${deploy_target}"
        suffix="${suffix} $(plugin-terraform-common "${deploy_target}")"
    fi

    if [[ "$(type -t "${deploy_target}-pre-deploy-terraform")" == function ]]; then
        echo "Running pre-deploy-terraform for ${deploy_target}"
        suffix="${suffix} $("${deploy_target}-pre-deploy-terraform")"
    fi

    # shellcheck disable=SC2086 # Intended globbing
    terraform apply ${suffix}

    mkdir -p "${RUNDIR}/../.deployment-temp/${DEPLOY_ENV}/terraform"
    terraform output -json > "${RUNDIR}/../.deployment-temp/${DEPLOY_ENV}/terraform/${deploy_target}-outputs.json"

    popd || exit 1
}

function destroy_terraform_impl() {
    local destroy_target="${1}"
    local deployment_dir="${2}"
    local is_plugin="${3}"

    pushd "${deployment_dir}" || exit 1

    terraform workspace select "${DEPLOY_ENV}"

    if [[ "${is_plugin}" == "false" ]]; then
        suffix="-var-file=../global.tfvars.json"
    else
        suffix=""
    fi

    if [ -f "${DEPLOY_ENV}.tfvars.json" ]; then
        suffix="${suffix} -var-file=${DEPLOY_ENV}.tfvars.json"
    fi

    if [ -f "${DEPLOY_ENV}-secret-values.tfvars" ]; then
        suffix="${suffix} -var-file=${DEPLOY_ENV}-secret-values.tfvars"
    fi

    if [[ "${is_plugin}" == "true" ]]; then
        echo "Running plugin-terraform-common for ${destroy_target}"
        suffix="${suffix} $(plugin-terraform-common "${destroy_target}")"
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
$(echo "${DEPLOYABLE_TARGETS}" | tr ' ' '\n' | sed -e 's/^/- /')

You can also pass DEPLOY_ENV env variable to choose
to which env changes should be applied
HEREDOC

    exit 1
}
