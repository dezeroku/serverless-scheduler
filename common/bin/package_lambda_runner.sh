#!/usr/bin/env bash
# This script is meant to be sourced from the entrypoint
# and is assumed to be run from proper component's directory

set -euo pipefail

DOCKERFILE_DIR="$(readlink -f "$(dirname "$0")")/.."

[ -z "${COMPONENT_NAME}" ] && echo "You have to provide COMPONENT_NAME" && exit 1

rm -rf ./.packaging
docker buildx build . -f "${DOCKERFILE_DIR}/Dockerfile" --build-arg "COMPONENT_NAME=${COMPONENT_NAME}" --output type=local,dest=./.packaging
