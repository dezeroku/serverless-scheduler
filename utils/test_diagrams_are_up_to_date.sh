#!/usr/bin/env bash
set -e

RUNDIR="$(readlink -f "$(dirname "$0")")"

DIAGRAMS_LOCATION="$(readlink -f "${RUNDIR}/../docs/diagrams")"

"${DIAGRAMS_LOCATION}"/build-docs

if [ -z "$(git status --porcelain -- "${DIAGRAMS_LOCATION}")" ] ; then
    echo "Diagrams are up-to-date!"
else
    echo "Python diagrams (docs/diagrams) are not in sync with generated .png images"
    echo "Run the docs/diagrams/build-docs to fix this"
    exit 1
fi
