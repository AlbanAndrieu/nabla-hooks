#!/bin/bash
#set -xve

WORKING_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && pwd  )"

# source only if terminal supports color, otherwise use unset color vars
# shellcheck source=/dev/null
#tput colors && source "${WORKING_DIR}/step-0-color.sh"
source "${WORKING_DIR}/step-0-color.sh"

echo -e "${green} Run bandit ${NC}"

mkdir "${WORKING_DIR}/../output" || true
#source /opt/ansible/env37/bin/activate
echo -e "${magenta} bandit -r ${WORKING_DIR}/../hooks/* -f xml -o ${WORKING_DIR}/../output/junit.xml --exclude static,templates,test,.eggs,.tox ${NC}"
bandit -r ${WORKING_DIR}/../hooks/* -f xml -o "${WORKING_DIR}/../output/junit.xml" --exclude static,templates,test,.eggs,.tox --skip B404,B607,B603
bandit -r ${WORKING_DIR}/../hooks/* -f html -o "${WORKING_DIR}/../output/bandit.html" --exclude static,templates,test,.eggs,.tox --skip B404,B607,B603

exit 0
