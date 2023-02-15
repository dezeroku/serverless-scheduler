#!/usr/bin/env bash
set -e

RUNDIR="$(readlink -f "$(dirname "$0")")"

SCHEMA_LOCATION="${RUNDIR}/../items/items/json_schemas.py"

"${RUNDIR}"/create_schemas.sh

if ! git diff-index --quiet HEAD -- "${SCHEMA_LOCATION}" ; then
    echo "Python JSON schemas (items/items/json_schemas.py) are not in sync with swagger definitions (items/swagger.yaml)!"
    echo "Run the utils/create_schemas.sh to fix this"
else
    echo "Schemas are up-to-date!"
fi
