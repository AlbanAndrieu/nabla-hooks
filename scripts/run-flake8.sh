#!/bin/bash
set -euo pipefail

WORKING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="${WORKING_DIR}/.."

# shellcheck source=/dev/null
source "${WORKING_DIR}/step-0-color.sh"

echo -e "${green} Run flake8 ${NC}"
flake8 --version

mkdir -p "${ROOT_DIR}/output"
# Report only, like the CI flake8 step (--exit-zero).
flake8 --exit-zero --config "${ROOT_DIR}/.flake8" "${ROOT_DIR}/hooks" --format=pylint --output-file "${ROOT_DIR}/output/flake8.txt"
