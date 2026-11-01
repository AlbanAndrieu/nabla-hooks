#!/bin/bash
# Source me (Jenkinsfile): installs the locked dependencies with uv and activates .venv.

if ! (return 0 2>/dev/null); then
  echo "This script has to be sourced and not executed..."
  exit 1
fi

WORKING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# shellcheck source=/dev/null
source "${WORKING_DIR}/step-0-color.sh"

# shellcheck source=/dev/null
source "${WORKING_DIR}/step-1-os.sh"

echo -e "${green} uv sync --locked ${NC}"
uv sync --locked --project "${WORKING_DIR}/.." || return 2

# shellcheck source=/dev/null
source "${WORKING_DIR}/../.venv/bin/activate" || return 2

python --version
