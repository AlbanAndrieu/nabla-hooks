#!/bin/bash
set -ex

# Convenience workspace directory for later use
WORKSPACE_DIR=$(pwd)

# Install Dependencies
# uv sync --no-cache

# Install pre-commit hooks
# uv run pre-commit install --install-hooks

export POETRY_VERSION=${POETRY_VERSION:-"2.2.1"}
pip install "poetry==${POETRY_VERSION}"

# Change some Poetry settings to better deal with working in a container
poetry config cache-dir "${WORKSPACE_DIR}/.cache"
poetry config virtualenvs.in-project true

# Now install all dependencies
poetry install --with format,test,extra,open_telemetry,api,deployment,influxdb,panda,temporal,utils,webui

echo "Done!"
