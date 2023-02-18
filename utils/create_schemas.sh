#!/usr/bin/env bash

RUNDIR="$(readlink -f "$(dirname "$0")")"

set -e
function create_schemas() {
    # Generate the .jsons
    pushd "$(mktemp -d)"
    openapi2jsonschema "${RUNDIR}/../items/swagger.yaml" --stand-alone

    pushd schemas

    for x in *.json; do
        var_name="${x%%.json}"
        var_name="${var_name##./}_schema"
        out_name="${x%%.json}.py"
        "${RUNDIR}/json2py.py" "${x}" "${out_name}" "${var_name}"
    done

    popd

    cat schemas/*.py | grep . > "${RUNDIR}/../items/items/json_schemas.py"
    popd
}

create_schemas
