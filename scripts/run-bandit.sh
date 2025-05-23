#!/bin/bash
#set -xve

WORKING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# shellcheck source=/dev/null
source "${WORKING_DIR}/../scripts/step-0-color.sh"

echo -e "${green} Run bandit ${NC}"

bandit --version

mkdir "${WORKING_DIR}/../output" || true
# shellcheck source=/dev/null
#source /opt/ansible/env38/bin/activate
echo -e "${magenta} bandit -r ${WORKING_DIR}/../hooks/* -f xml -o ${WORKING_DIR}/../output/junit-bandit.xml --exclude static,templates,test,hooks/test,.eggs,.tox ${NC}"
bandit -r "${WORKING_DIR}/../hooks/*" -f xml -o "${WORKING_DIR}/../output/junit-bandit.xml" --exclude static,templates,test,hooks/tests,.eggs,.tox --skip B404,B607,B603,B101
bandit -r "${WORKING_DIR}/../hooks/*" -f html -o "${WORKING_DIR}/../output/bandit.html" --exclude static,templates,test,hooks/tests,.eggs,.tox --skip B404,B607,B603,B101

echo -e "${magenta} bandit-config-generator --out bandit.yml ${NC}"
echo -e "${magenta} bandit --ini .bandit  --configfile .bandit.yml -r hooks ${NC}"
echo -e "${magenta} bandit -c .bandit.yml -r hooks ${NC}"

echo -e "${magenta} bandit -c .bandit.yml -r hooks -f xml -o bandit-output.xml ${NC}"
echo -e "${magenta} bandit -c .bandit.yml -r hooks -f json  -o bandit-output.json ${NC}"

exit 0
