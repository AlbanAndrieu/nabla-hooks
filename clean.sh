#!/bin/bash
#set -xv

rm -Rf _build/ build/ .eggs/ .toxs/ dist/ pytest.xml .coverage coverage.xml docs/_build/ .tox/ .scannerwork/ .pytest_cache/ htmlcov/ cprofile

find . -maxdepth 2 -mindepth 2 -regextype posix-egrep -type d -regex '.+/.*egg-info' -exec rm -rf {} \;
find . -maxdepth 2 -mindepth 2 -regextype posix-egrep -type d -regex '.*__pycache__.*' -exec rm -rf {} \;
find hooks -type f -name "*.pyc" -delete

#/**/*.egg-info/ **/__pycache__/
#lib/

exit 0
