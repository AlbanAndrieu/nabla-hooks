#!/bin/bash
#set -e

WORKING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# shellcheck source=/dev/null
source "${WORKING_DIR}/step-0-color.sh"

# curl (REST API)
# Assuming "anonymous read access" has been enabled on your Jenkins instance.
# JENKINS_URL=[root URL of Jenkins master]
if [ -n "${JENKINS_URL}" ]; then
  echo -e "${green} JENKINS_URL is defined ${happy_smiley} : ${JENKINS_URL} ${NC}"
else
  echo -e "${red} ${double_arrow} Undefined build parameter ${head_skull} : JENKINS_URL, use the default one ${NC}"
  JENKINS_URL="https://localhost/"
  export JENKINS_URL
  echo -e "${magenta} JENKINS_URL : ${JENKINS_URL} ${NC}"
fi

if [ -f ${HOME}/jenkins-cli.jar ]; then
  echo "jenkins-cli.jar file found"
  # Get randomly assigned SSH port
  echo -e "${green} curl -Lv $JENKINS_URL/login 2>&1 | grep -i 'x-ssh-endpoint' ${NC}"
  # Configure user
  echo -e "${JENKINS_URL}/me/configure ${NC}"
  echo -e "${green} java -jar ${HOME}/jenkins-cli.jar -s ${JENKINS_URL} -auth ${JENKINS_USER}:${JENKINS_USER_TOKEN} who-am-i ${NC}"
  #echo -e "${green} java -jar ${HOME}/jenkins-cli.jar -s ${JENKINS_URL} -auth username:password list-jobs ${NC}"
else
  wget --no-check-certificate ${JENKINS_URL}/jnlpJars/jenkins-cli.jar --directory-prefix=${HOME}
fi

JENKINS_FILE=$1

if [ -n "${JENKINS_FILE}" ]; then
  echo -e "${green} JENKINS_FILE is defined ${happy_smiley} : ${JENKINS_FILE} ${NC}"
else
  echo -e "${red} ${double_arrow} Undefined build parameter ${head_skull} : JENKINS_FILE, use the default one ${NC}"
  JENKINS_FILE="Jenkinsfile"
  export JENKINS_FILE
  echo -e "${magenta} JENKINS_FILE : ${JENKINS_FILE} ${NC}"
fi

# In atom
# ssh -p 22 -i ~/.ssh/id_rsa root@jenkins sudo java -jar ${HOME}/jenkins-cli.jar -s ${JENKINS_URL} declarative-linter < ${JENKINS_FILE}

echo -e "${green} Running the jenkins validation. ${NC}"

# JENKINS_CRUMB is needed if your Jenkins master has CRSF protection enabled as it should
JENKINS_CRUMB=$(curl "$JENKINS_URL/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,\":\",//crumb)")
# shellcheck disable=SC2145
echo -e "${magenta} curl -X POST -H \"$JENKINS_CRUMB\" -F \"jenkinsfile=<${JENKINS_FILE}\" \"$JENKINS_URL/pipeline-model-converter/validate\" \"$@\" ${NC}"
curl -X POST -H "$JENKINS_CRUMB" -F "jenkinsfile=<${JENKINS_FILE}" "$JENKINS_URL/pipeline-model-converter/validate"
RC=$?
if [ ${RC} -ne 0 ]; then
  echo ""
  # shellcheck disable=SC2154
  echo -e "${red} ${head_skull} Sorry, jenkins validation failed. ${NC}"
  exit 1
else
  # shellcheck disable=SC2154
  echo -e "${green} Jenkins validated. ${NC}"
fi

# ssh (Jenkins CLI)
# JENKINS_SSHD_PORT=[sshd port on master]
#JENKINS_SSHD_PORT=222
# JENKINS_HOSTNAME=[Jenkins master hostname]
#JENKINS_HOSTNAME=localhost
#ssh -p $JENKINS_SSHD_PORT $JENKINS_HOSTNAME declarative-linter < Jenkinsfile

exit 0
