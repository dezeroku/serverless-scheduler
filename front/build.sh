#!/usr/bin/env bash
set -euo pipefail

rm -rf .packaging

output_dir="./.packaging/result"
docker buildx build . --target build-files --output "type=local,dest=${output_dir}"
