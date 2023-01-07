#!/usr/bin/env bash
# This script is meant to be sourced from the entrypoint
# and is assumed to be run from proper component's directory

set -euo pipefail

DOCKERFILE_DIR="$(readlink -f "$(dirname "$0")/..")"

[ -z "${COMPONENT_NAME}" ] && echo "You have to provide COMPONENT_NAME" && exit 1

# Make sure that common module wheel is in place
# and generate a final zip with component's + common content inside
# This is meant to be run after component's initial generation is done

# shellcheck disable=SC2086 # Intended globbing
cp ${DOCKERFILE_DIR}/.packaging/work/*.whl "${PWD}/.packaging/work"

docker buildx build . --target concatenate -f "${DOCKERFILE_DIR}/Dockerfile" --build-arg "COMPONENT_NAME=${COMPONENT_NAME}" --output type=local,dest=./.packaging/result
