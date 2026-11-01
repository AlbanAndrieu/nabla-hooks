#!/bin/bash
set -euo pipefail

echo -e "${cyan:-} uv sync --locked ${NC:-}"
uv sync --locked
