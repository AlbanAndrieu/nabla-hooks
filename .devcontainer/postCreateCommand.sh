#!/bin/bash
set -ex

# Install all dependency groups from uv.lock into .venv
uv sync --locked --all-groups

# Install pre-commit hooks
uv run pre-commit install --install-hooks

echo "Done!"
