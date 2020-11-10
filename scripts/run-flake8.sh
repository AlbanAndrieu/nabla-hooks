#!/bin/bash
#set -xve

WORKING_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && pwd  )"

# shellcheck source=/dev/null
source "${WORKING_DIR}/../scripts/step-0-color.sh"

echo -e "${green} Run Pylint ${NC}"

flake8 --version

mkdir "${WORKING_DIR}/../output" || true

# shellcheck source=/dev/null
#source /opt/ansible/env38/bin/activate
echo -e "${magenta} flake8 --ignore E24,W504 ${WORKING_DIR}/../hooks/ --format=pylint --output-file ${WORKING_DIR}/../output/flake8.txt ${NC}"
flake8 --ignore E24,W504 ${WORKING_DIR}/../hooks/ --format=pylint --output-file ${WORKING_DIR}/../output/flake8.txt

exit 0
