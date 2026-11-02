#!/bin/bash
set -euo pipefail

WORKING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# shellcheck source=/dev/null
source "${WORKING_DIR}/step-0-color.sh"

# Python version pinned in mise.toml; any env of tox.ini envlist works.
TOX_TARGET=${TOX_TARGET:-"py314"}

echo -e "${magenta} tox -e ${TOX_TARGET} ${NC}"
if ! tox -e "${TOX_TARGET}"; then
  echo -e "${red} ${head_skull:-} Sorry, test failed. ${NC}"
  exit 1
fi
echo -e "${green} The build completed successfully. ${NC}"
