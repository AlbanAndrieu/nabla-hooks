#!/bin/bash
#set -xv

#WORKING_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && pwd  )"

# shellcheck source=./docs/build.sh
#echo "${WORKING_DIR}/docs/build.sh"

# shellcheck source=./scripts/run-python.sh
# echo "${WORKING_DIR}/scripts/run-python.sh"

# shellcheck source=./clean.sh
#${WORKING_DIR}/clean.sh"

export TOX_TARGET=${TOX_TARGET:-""} # tox --notest  # Pre-populate virtualenv use TOX_TARGET

export PATH="${VIRTUALENV_PATH}/bin:${PATH}"
echo -e "${cyan} PATH : ${PATH} ${NC}"
export PYTHONPATH="${VIRTUALENV_PATH}/lib/python${PYTHON_MAJOR_VERSION}/site-packages/"
echo -e "${cyan} PYTHONPATH : ${PYTHONPATH} ${NC}"

python -V || true

#pip install --upgrade pip

#pip install setup-py-upgrade
#pip install setup-cfg-fmt

#pip install coverage==4.5.3
coverage --version || true

#setup-py-upgrade ./
setup-cfg-fmt setup.cfg

export TOXENV=py36
#pip install -U tox
#pip install tox==3.14.0

tox ${TOX_TARGET}
RC=$?
if [ ${RC} -ne 0 ]; then
  echo ""
  echo -e "${red} ${head_skull} Sorry, build failed. ${NC}"
  exit 1
else
  echo -e "${green} The build completed successfully. ${NC}"
fi

#./test/init.sh
#RC=$?
#if [ ${RC} -ne 0 ]; then
#  echo ""
#  echo -e "${red} ${head_skull} Sorry, test failed. ${NC}"
#  exit 1
#else
#  echo -e "${green} The test completed successfully. ${NC}"
#fi

#python3 setup.py sdist bdist_wheel
#RC=$?
#if [ ${RC} -ne 0 ]; then
#  echo ""
#  echo -e "${red} ${head_skull} Sorry, package failed. ${NC}"
#  exit 1
#else
#  echo -e "${green} The package completed successfully. ${NC}"
#fi

#git tag --delete v1.0.0
#git push --delete origin v1.0.0
echo -e "git tag v1.0.0"
echo -e "git push origin --tags"

exit 0
