#!/bin/bash
#set -xv

WORKING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# shellcheck source=/dev/null
source "${WORKING_DIR}/scripts/step-0-color.sh"

# shellcheck source=/dev/null
source "${WORKING_DIR}/scripts/step-1-os.sh"

export REPO_TAG=${REPO_TAG:-"1.0.6"}

# shellcheck source=./docs/build.sh
#echo "${WORKING_DIR}/docs/build.sh"

# shellcheck source=./scripts/run-python.sh
# echo "${WORKING_DIR}/scripts/run-python.sh"

# shellcheck source=./clean.sh
#${WORKING_DIR}/clean.sh"

echo -e "${cyan} ${WORKING_DIR}/scripts/run-install.sh ${NC}"
# "${WORKING_DIR}/scripts/run-install.sh"

#pipenv install

export TOX_TARGET=${TOX_TARGET:-"py312"} # tox --notest  # Pre-populate virtualenv use TOX_TARGET

#export PATH="${VIRTUALENV_PATH}/bin:${PATH}"
echo -e "${cyan} PATH : ${PATH} ${NC}"
#export PYTHONPATH="${VIRTUALENV_PATH}/lib/python${PYTHON_MAJOR_VERSION}/site-packages/"
echo -e "${cyan} PYTHONPATH : ${PYTHONPATH} ${NC}"

python -V || true

#pip install coverage==4.5.3
coverage --version || true

#setup-py-upgrade ./
echo -e "${magenta} setup-cfg-fmt setup.cfg ${NC}"
setup-cfg-fmt setup.cfg

"${WORKING_DIR}/scripts/run-test.sh"

echo -e "${magenta} unset JAVA_HOME ${NC}"
echo -e "${magenta} /usr/local/sonar-runner/bin/sonar-scanner -Dproject.settings=./sonar-project.properties -Dsonar.scanner.force-deprecated-java-version=true ${NC}"
echo -e "${cyan} https://sonarcloud.io/dashboard?id=nabla%3Anabla-hooks ${NC}"

echo -e "${magenta} Change hooks/__init__.py version ${NC}"

#git tag --delete v1.0.0
#git push --delete origin v1.0.0
echo -e "${magenta} git tag v${REPO_TAG} ${NC}"
echo -e "${magenta} git push origin --tags ${NC}"

echo -e "${cyan} PACKAGE ${NC}"

echo -e "${cyan} pandoc --from=markdown --to=rst --output=README.rst README.md ${NC}"

# See https://github.com/python-versioneer/python-versioneer/blob/master/INSTALL.md
echo -e "${cyan} versioneer install --vendor ${NC}"
echo -e "${cyan} Verify versioneer version ${NC}"
python setup.py version

echo -e "${cyan} python setup.py sdist bdist_wheel ${NC}"
python setup.py sdist bdist_wheel

echo -e "${cyan} install locally ${NC}"
python3 setup.py install

git tags
git describe --tag --dirty

echo -e "${cyan} test locally ${NC}"
python ./bin/get_msg test

echo -e "${cyan} test locally with pytest ${NC}"
pytest --cache-clear --setup-show tests/test_package.py

echo -e "${magenta} twine upload dist/* ${NC}"

echo -e "${cyan} https://pypi.org/project/nabla-hooks/${REPO_TAG}/ ${NC}"

exit 0
