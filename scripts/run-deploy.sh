#!/bin/bash
set -euo pipefail

WORKING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# shellcheck source=/dev/null
source "${WORKING_DIR}/step-0-color.sh"

echo -e "${green} uv build (sdist and wheel in dist/) ${NC}"
if ! uv build --project "${WORKING_DIR}/.."; then
  echo -e "${red} ${head_skull} Sorry, package failed. ${NC}"
  exit 1
fi
echo -e "${green} The package completed successfully. ${NC}"
