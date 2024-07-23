#!/bin/bash
#set -xv

#WORKING_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && pwd  )"

# shellcheck source=./docs/build.sh
#echo "${WORKING_DIR}/docs/build.sh"

# shellcheck source=./scripts/run-python.sh
# echo "${WORKING_DIR}/scripts/run-python.sh"

#pip uninstall pylint pytest tox setup-cfg-fmt molecule yamllint pip-upgrade ansible

#source /opt/ansible/env38/bin/activate

echo -e "${magenta} sudo apt install ruby gem ${NC}"

#echo -e "${magenta} rm -Rf /home/albanandrieu/.pyenv ${NC}"
#echo -e "${magenta} curl -L https://pyenv.run | bash ${NC}"

echo -e "${magenta} pyenv update ${NC}"
echo -e "${magenta} pyenv install 3.8.19 ${NC}"
echo -e "${magenta} pyenv install 3.10.9 ${NC}"

echo -e "${magenta} /opt/ansible/env38/bin/pip3.8 install pip-upgrader ${NC}"
echo -e "${magenta} pip-upgrade --user hooks/requirements-current-3.8.txt ${NC}"
echo -e "${magenta} pip-upgrade requirements.testing.txt ${NC}"

echo -e "${magenta} pip install -r ./requirements.txt -r requirements.testing.txt ${NC}"
pip install -r ./requirements.txt -r requirements.testing.txt

echo -e "${magenta} pip install --upgrade pip ${NC}"

#pip install setup-py-upgrade
#pip install setup-cfg-fmt

#pip install --upgrade setuptools
echo -e "${magenta} pip install setuptools wheel twine ${NC}"

echo -e "${cyan} poetry update ${NC}"
#echo -e "${cyan} poetry install ${NC}"
poetry install

exit 0
