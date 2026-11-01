#!/usr/bin/env bash
set -euo pipefail

WORKING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# shellcheck source=/dev/null
source "${WORKING_DIR}/step-0-color.sh"

# Validates a declarative Jenkinsfile with the Jenkins REST API (anonymous read access).
# You can test it with
# JENKINS_URL=https://jenkins.example.com pre_commit_hooks/jenkinsfile-check.sh Jenkinsfile

JENKINS_FILE=${1:-Jenkinsfile}

if [ -z "${JENKINS_URL:-}" ]; then
  echo -e "${yellow} ${double_arrow} JENKINS_URL is not set, skipping the validation of ${JENKINS_FILE} ${NC}"
  exit 0
fi

echo -e "${green} Running the jenkins validation of ${JENKINS_FILE} on ${JENKINS_URL} ${NC}"

# The CSRF crumb is bound to the session: keep its cookie for the POST.
cookie_jar=$(mktemp)
trap 'rm -f "${cookie_jar}"' EXIT

jenkins_crumb=$(curl -fsS -c "${cookie_jar}" "${JENKINS_URL}/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,\":\",//crumb)")
result=$(curl -fsS -b "${cookie_jar}" -X POST -H "${jenkins_crumb}" -F "jenkinsfile=<${JENKINS_FILE}" "${JENKINS_URL}/pipeline-model-converter/validate")
echo "${result}"

# The endpoint answers 200 even for an invalid Jenkinsfile.
if [[ "${result}" != *"successfully validated"* ]]; then
  echo -e "${red} ${head_skull} Sorry, jenkins validation failed. ${NC}"
  exit 1
fi
echo -e "${green} Jenkins validated. ${NC}"
