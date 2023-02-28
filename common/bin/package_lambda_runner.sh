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

# If INTERMEDIATE_PACKAGING==true you need to also run package_lambda_concatenate.sh to get a proper zip
# If it's set to true, it's assumed that you either use a Lambda layer for the 'common' package or you don't use the common package at all
if [[ "${INTERMEDIATE_PACKAGING:-false}" == "true" ]]; then
    output_dir="./.packaging/work"
else
    output_dir="./.packaging/result"
fi

if [[ "${GHA_DOCKER_CACHING:-false}" == "true" ]]; then
    EXTRA_ARGS="--cache-to type=gha,mode=max --cache-from type=gha"
fi

# You may want to use CUSTOM_PACKAGING_DIRECTORY when you want to package the zip to a directory with some prefix
# e.g. in case of Lambda layers that use python, the final zip should be unpacked to /opt/python, but without the `python` prefix it
# will land just in /opt
#
# shellcheck disable=SC2086 # Intended globbing
docker buildx build . --target zip -f "${DOCKERFILE_DIR}/Dockerfile" --build-arg "CUSTOM_PACKAGING_DIRECTORY=${CUSTOM_PACKAGING_DIRECTORY:-}" --build-arg "COMPONENT_NAME=${COMPONENT_NAME}" --output "type=local,dest=${output_dir}" ${EXTRA_ARGS:-}
