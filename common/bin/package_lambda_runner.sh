#!/usr/bin/env bash
# This script is meant to be sourced from the entrypoint
# and is assumed to be run from proper component's directory

set -euo pipefail

DOCKERFILE_DIR="$(readlink -f "$(dirname "$0")/..")"

[ -z "${COMPONENT_NAME}" ] && echo "You have to provide COMPONENT_NAME" && exit 1

rm -rf ./.packaging

# Dirty hack to work around common relative path until https://github.com/python-poetry/poetry/issues/668 gets proper solution
mkdir -p .packaging/temp
if [[ ! "$PWD" == "${DOCKERFILE_DIR}" ]]; then
  cp -r "${DOCKERFILE_DIR}/common" .packaging/temp
  cp "${DOCKERFILE_DIR}/pyproject.toml" .packaging/temp
  cp "${DOCKERFILE_DIR}/poetry.lock" .packaging/temp
fi

docker buildx build . -f "${DOCKERFILE_DIR}/Dockerfile" --build-arg "COMPONENT_NAME=${COMPONENT_NAME}" --output type=local,dest=./.packaging/result
