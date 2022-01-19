#!/bin/bash
#set -xve

WORKING_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && pwd  )"

# shellcheck source=/dev/null
source "${WORKING_DIR}/../scripts/step-0-color.sh"

echo -e "${green} Run Pylint ${NC}"

pylint --version

mkdir "${WORKING_DIR}/../output" || true

# shellcheck source=/dev/null
#source /opt/ansible/env38/bin/activate
echo -e "${magenta} pylint ${WORKING_DIR}/../hooks/ --output-format=parseable > ${WORKING_DIR}/../output/pylint.txt ${NC}"
pylint ${WORKING_DIR}/../hooks/* --output-format=parseable > ${WORKING_DIR}/../output/pylint.txt

echo -e "${magenta} pylint $(find ./hooks -name "*.py" -type f -print0 | xargs) ${NC}"

exit 0
