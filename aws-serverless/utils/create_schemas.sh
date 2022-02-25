#!/usr/bin/env bash

RUNDIR="$(readlink -f $(dirname "$0"))"

set -e
function create_schemas() {
    # Generate the .jsons
    pushd common
    openapi2jsonschema ../swagger/swagger.yaml --stand-alone

    # Make the .jsons part of .py
    rm -f schemas.py

    pushd schemas

    for x in $(find . -name "*.json"); do
        var_name="${x%%.json}"
        var_name="${var_name##./}_schema"
        out_name="${x%%.json}.py"
        "${RUNDIR}/json2py.py" $x $out_name $var_name
    done

    popd

    cat schemas/*.py > schemas.py
    popd
}

# TODO: We likely need to create a separate job for validating the commited schemas with generated ones
create_schemas
