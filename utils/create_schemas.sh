#!/usr/bin/env bash

RUNDIR="$(readlink -f "$(dirname "$0")")"

set -e
function create_schemas() {
    # Generate the .jsons
    pushd "$(mktemp -d)"
    openapi2jsonschema "${RUNDIR}/../swagger/swagger.yaml" --stand-alone

    pushd schemas

    for x in *.json; do
        var_name="${x%%.json}"
        var_name="${var_name##./}_schema"
        out_name="${x%%.json}.py"
        "${RUNDIR}/json2py.py" "${x}" "${out_name}" "${var_name}"
    done

    popd

    cat schemas/*.py > "${RUNDIR}/../common/common/json_schemas.py"
    popd
}

# TODO: We likely need to create a separate job for validating the commited schemas with generated ones
create_schemas
