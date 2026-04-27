#!/bin/bash
#set -xv

rm -Rf _build/ build/ .eggs/ .toxs/ dist/ output/pytest-report.xml .coverage output/coverage.xml coverage.xml docs/_build/ .tox/ .scannerwork/ .pytest_cache/ pytest-report.xml output/htmlcov/ cprofile

find . -maxdepth 2 -mindepth 2 -regextype posix-egrep -type d -regex '.+/.*egg-info' -exec rm -rf {} \;
find . -maxdepth 2 -mindepth 2 -regextype posix-egrep -type d -regex '.*__pycache__.*' -exec rm -rf {} \;
find hooks -type f -name "*.pyc" -delete

rm -Rf output/ || true
mkdir output || true

#lib/

exit 0
