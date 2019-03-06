#!/bin/bash
#set -xv

WORKING_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && pwd  )"

# shellcheck source=./docs/build.sh
"${WORKING_DIR}/docs/build.sh"

#pip install setup-py-upgrade
#pip install setup-cfg-fmt

#setup-py-upgrade ./
setup-cfg-fmt setup.cfg

tox

#pip install pyinstaller
#pyinstaller hooks/get_msg.py

python3 setup.py sdist bdist_wheel

./test/init.sh

#git tag --delete v1.0.0
#git push --delete origin v1.0.0
echo -e "git tag v1.0.0"
echo -e "git push origin --tags"

exit 0
