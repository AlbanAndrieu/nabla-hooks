#!/bin/bash
#set -xv

WORKING_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && pwd  )"

# shellcheck source=./docs/build.sh
#echo "${WORKING_DIR}/docs/build.sh"

# shellcheck source=./scripts/run-python.sh
# echo "${WORKING_DIR}/scripts/run-python.sh"

# shellcheck source=./clean.sh
#${WORKING_DIR}/clean.sh"

#./run-install.sh

#export PATH="${VIRTUALENV_PATH}/bin:${PATH}"
echo -e "${cyan} PATH : ${PATH} ${NC}"
#export PYTHONPATH="${VIRTUALENV_PATH}/lib/python${PYTHON_MAJOR_VERSION}/site-packages/"
echo -e "${cyan} PYTHONPATH : ${PYTHONPATH} ${NC}"

python -V || true

#pip install coverage==4.5.3
coverage --version || true

#setup-py-upgrade ./
setup-cfg-fmt setup.cfg

${WORKING_DIR}/run-test.sh

echo -e "${magenta} /usr/local/sonar-runner/bin/sonar-scanner -Dproject.settings=./sonar-project.properties -Dsonar.scanner.force-deprecated-java-version=true ${NC}"

#git tag --delete v1.0.0
#git push --delete origin v1.0.0
echo -e "${magenta} git tag v1.0.0 ${NC}"
echo -e "${magenta} git push origin --tags ${NC}"

exit 0
