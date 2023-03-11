#!/usr/bin/env bash
set -e

RUNDIR="$(readlink -f "$(dirname "$0")")"

SCHEMA_LOCATION="$(readlink -f "${RUNDIR}/../items/items/json_schemas.py")"

pushd "${RUNDIR}/.."

"${RUNDIR}"/create_schemas.sh

if [ -z "$(git status --porcelain -- "${SCHEMA_LOCATION}")" ] ; then
    echo "Schemas are up-to-date!"
else
    echo "Python JSON schemas (items/items/json_schemas.py) are not in sync with swagger definitions (items/swagger.yaml)!"
    echo "Run the utils/create_schemas.sh to fix this"
    exit 1
fi
