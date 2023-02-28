#!/usr/bin/env bash
set -euo pipefail

rm -rf .packaging

output_dir="./.packaging/result"

if [[ "${GHA_DOCKER_CACHING:-false}" == "true" ]]; then
    EXTRA_ARGS="--cache-to type=gha,mode=max --cache-from type=gha"
fi

# shellcheck disable=SC2086 # Intended globbing
docker buildx build . --target build-files --output "type=local,dest=${output_dir}" ${EXTRA_ARGS:-}
