#!/bin/bash
set -euo pipefail

WORKING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="${WORKING_DIR}/.."

# shellcheck source=/dev/null
source "${WORKING_DIR}/step-0-color.sh"

echo -e "${green} Run pylint ${NC}"
pylint --version

mkdir -p "${ROOT_DIR}/output"
# Report only: ruff is the blocking linter, pylint feeds output/pylint.txt.
pylint "${ROOT_DIR}/hooks" --output-format=parseable >"${ROOT_DIR}/output/pylint.txt" || true
tail -n 3 "${ROOT_DIR}/output/pylint.txt"
