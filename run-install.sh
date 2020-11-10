#!/bin/bash
#set -xv

#WORKING_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && pwd  )"

# shellcheck source=./docs/build.sh
#echo "${WORKING_DIR}/docs/build.sh"

# shellcheck source=./scripts/run-python.sh
# echo "${WORKING_DIR}/scripts/run-python.sh"

pip uninstall pylint pytest tox setup-cfg-fmt molecule yamllint pip-upgrade ansible

#source /opt/ansible/env38/bin/activate

echo -e "${magenta} /opt/ansible/env38/bin/pip3.8 install pip-upgrader ${NC}"
echo -e "${magenta} pip-upgrade --user hooks/requirements-current-3.8.txt ${NC}"
echo -e "${magenta} pip-upgrade requirements.testing.txt ${NC}"

echo -e "${magenta} pip install -r ./requirements.txt -r requirements.testing.txt ${NC}"
#pip install -r ./requirements.txt -r requirements.testing.txt

#pip install --upgrade pip

#pip install setup-py-upgrade
#pip install setup-cfg-fmt

#pip install --upgrade setuptools
#pip install setuptools wheel twine

exit 0
