#!/bin/bash
#set -xv

rm -Rf _build/ build/ .eggs/ .toxs/ dist/ output/pytest-report.xml .coverage output/coverage.xml docs/_build/ .tox/ .scannerwork/ .pytest_cache/ output/htmlcov/ cprofile
rm -Rf pytest-report.xml coverage.xml

find . -maxdepth 2 -mindepth 2 -regextype posix-egrep -type d -regex '.+/.*egg-info' -exec rm -rf {} \;
find . -maxdepth 2 -mindepth 2 -regextype posix-egrep -type d -regex '.*__pycache__.*' -exec rm -rf {} \;
find hooks -type f -name "*.pyc" -delete

mkdir output || true

#lib/

exit 0
