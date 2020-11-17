#!/bin/bash
#set -xv

#WORKING_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && pwd  )"

export TOX_TARGET=${TOX_TARGET:-"py38"} # tox --notest  # Pre-populate virtualenv use TOX_TARGET

export TOXENV=${TOXENV:-"py38"}
#pip install -U tox
#pip install tox==3.14.3

#tox -e py  # Run tox using the version of Python in `PATH`

rm -Rf .tox/
echo -e "${magenta} tox ${TOX_TARGET} ${NC}"
tox ${TOX_TARGET}
RC=$?
if [ ${RC} -ne 0 ]; then
  echo ""
  echo -e "${red} ${head_skull} Sorry, test failed. ${NC}"
  exit ${RC}
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

exit 0
