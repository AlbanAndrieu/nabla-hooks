#!/bin/bash
#set -xv

mkdir output || true
source /opt/ansible/env36/bin/activate
bandit -r -f xml -o output/junit.xml .
bandit -r -f html -o output/bandit.html .

exit 0
