#!/bin/bash
#set -xv

WORKING_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && pwd  )"

# shellcheck source=../run-python.sh
# echo "${WORKING_DIR}/../scripts/run-python.sh"

# shellcheck source=/dev/null
# shellcheck disable=SC1091
source /opt/ansible/env36/bin/activate

#sphinx-quickstart
sphinx-build -b html ${WORKING_DIR}/ ${WORKING_DIR}/_build/
# or make html
RC=$?
if [ ${RC} -ne 0 ]; then
  echo ""
  echo -e "${red} ${head_skull} Sorry, build failed. ${NC}"
  exit 1
else
  echo -e "${green} The build completed successfully. ${NC}"
fi

exit 0
