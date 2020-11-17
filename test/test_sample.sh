#!/bin/bash
#set -eu

WORKING_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && pwd  )"

# shellcheck source=/dev/null
source "${WORKING_DIR}/../scripts/step-0-color.sh"

echo -e "${green} Run Test ${NC}"

cd "${WORKING_DIR}/../hooks" || exit
python3 -m get_jira.get_jira TESTME feature/BMT-13403 -v
python3 -m get_jira.get_auth -u aandrieu -p XXXX -v
cd "${WORKING_DIR}" || exit
${WORKING_DIR}/../hooks/get_msg.py '../.git/COMMIT_EDITMSG'

exit 0
