#!/bin/bash
set -euo pipefail

WORKING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="${WORKING_DIR}/.."

# shellcheck source=/dev/null
source "${WORKING_DIR}/step-0-color.sh"

echo -e "${green} Run bandit ${NC}"
bandit --version

mkdir -p "${ROOT_DIR}/output"
# Excludes and skipped tests live in .bandit.yml.
bandit -c "${ROOT_DIR}/.bandit.yml" -r "${ROOT_DIR}/hooks" -f xml -o "${ROOT_DIR}/output/junit-bandit.xml"
bandit -c "${ROOT_DIR}/.bandit.yml" -r "${ROOT_DIR}/hooks" -f html -o "${ROOT_DIR}/output/bandit.html"
