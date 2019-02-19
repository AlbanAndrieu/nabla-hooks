#!/bin/bash
#set -xv

WORKING_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && pwd  )"

# shellcheck source=./docs/build.sh
"${WORKING_DIR}/docs/build.sh"

python3 setup.py sdist bdist_wheel

echo -e "git tag v1.0.0"
echo -e "git push origin --tags"

exit 0
