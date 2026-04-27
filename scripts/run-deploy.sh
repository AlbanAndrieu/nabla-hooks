#!/bin/bash
#set -xv

WORKING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# sudo python setup.py develop

echo -e "${magenta} OLD way to build and install package... ${NC}"
echo -e "${magenta} python3 Builds sdist: ${NC}"
echo -e "python3 setup.py sdist"
echo -e "${magenta} Builds wheels: ${NC}"
echo -e "python3 setup.py bdist_wheel"
echo -e "${magenta} Build from source: ${NC}"
echo -e "python3 setup.py build"

echo -e "${magenta} And install: ${NC}"
echo -e "python3 setup.py install"

echo -e "${green} Build ${NC}"
python -m build
RC=$?
if [ ${RC} -ne 0 ]; then
  echo ""
  echo -e "${red} ${head_skull} Sorry, package failed. ${NC}"
  exit 1
else
  echo -e "${green} The package completed successfully. ${NC}"
fi

exit 0
