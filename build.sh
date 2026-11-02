#!/bin/bash
set -euo pipefail

WORKING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# shellcheck source=/dev/null
source "${WORKING_DIR}/scripts/step-0-color.sh"

export REPO_TAG=${REPO_TAG:-"1.0.7"}

"${WORKING_DIR}/scripts/run-install.sh"
"${WORKING_DIR}/scripts/run-test.sh"
"${WORKING_DIR}/scripts/run-deploy.sh"

echo -e "${cyan} test the package ${NC}"
uv run --project "${WORKING_DIR}" pytest --cache-clear "${WORKING_DIR}/tests/test_package.py"

git -C "${WORKING_DIR}" describe --tags --dirty --always --long

echo -e "${magenta} To release: git tag v${REPO_TAG} && git push origin --tags && uv publish ${NC}"
echo -e "${cyan} https://pypi.org/project/nabla-hooks/${REPO_TAG}/ ${NC}"
