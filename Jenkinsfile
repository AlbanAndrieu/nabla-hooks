#!/usr/bin/env groovy
@Library('jenkins-pipeline-scripts') _

/*
 * Fusion Risk Ansible
 *
 * Test Ansible Playbooks by: ansible-lint, ansible-playbook on docker images
 */

def DOCKER_REGISTRY="docker.hub"
def DOCKER_ORGANISATION="nabla"
def DOCKER_TAG="latest"
def DOCKERNAME="ansible-jenkins-slave"

def DOCKER_REGISTRY_URL="https://${DOCKER_REGISTRY}"
def DOCKER_REGISTRY_CREDENTIAL='jenkins'
def DOCKER_IMAGE="${DOCKER_REGISTRY}/${DOCKER_ORGANISATION}/${DOCKER_NAME}:${DOCKER_TAG}"

def DOCKER_OPTS = [
  '--dns-search=nabla.mobi',
  '-v /etc/passwd:/etc/passwd:ro ',
  '-v /etc/group:/etc/group:ro '
].join(" ")

pipeline {
  agent {
    label 'ansible-check'
  }
  parameters {
    string(name: 'DRY_RUN', defaultValue: '--check', description: 'Default mode used to test playbook')
    booleanParam(name: 'CLEAN_RUN', defaultValue: false, description: 'Clean before run')
  }
  environment {
    JENKINS_CREDENTIALS = 'jenkins-ssh'
    DRY_RUN = "${params.DRY_RUN}"
    CLEAN_RUN = "${params.CLEAN_RUN}"
    DEBUG_RUN = "${params.DEBUG_RUN}"
    BRANCH_NAME = "${env.BRANCH_NAME}".replaceAll("feature/","")
    PROJECT_BRANCH = "${env.GIT_BRANCH}".replaceFirst("origin/","")
    BUILD_ID = "${env.BUILD_ID}"
  }
  options {
    disableConcurrentBuilds()
    skipStagesAfterUnstable()
    parallelsAlwaysFailFast()       
    ansiColor('xterm')
    timeout(time: 360, unit: 'MINUTES')
    timestamps()
  }
  stages {
    stage('Setup') {
      steps {
        script {
          properties(createPropertyList())
          setBuildName()
          if (! isReleaseBranch()) { abortPreviousRunningBuilds() }
        }
      }
    }
    stage('Documentation') {
      // Creates documentation using Sphinx and publishes it on Jenkins
      // Copy of the documentation is rsynced with kgrdb01
      steps {
        script {
          dir("docs") {
            sh "source /opt/ansible/env36/bin/activate && make html"
          }
          publishHTML([
            allowMissing: false,
            alwaysLinkToLastBuild: false,
            keepAll: true,
            reportDir: "./docs/_build/html/",
            reportFiles: 'index.html',
            includes: '**/*',
            reportName: 'Sphinx Docs',
            reportTitles: "Sphinx Docs Index"
          ])
          if (isReleaseBranch()) {
            // Initially, we will want to publish only one version,
            // i.e. the latest one from develop branch.
            dir("docs/_build/html") {
              rsync([
                source: "*",
                destination: "jenkins@albandri:/nabla/release/docs/nabla-hooks/",
                credentialsId: "jenkins_unix_slaves"
              ])
            }
          }
        }
      }
    }
    stage("Bandit Report") {
      agent {
        label 'ansible-check&&ubuntu&&!albandri&&!trottt'
      }
      when {
        expression { BRANCH_NAME ==~ /(release|master|develop)/ }
      }
      steps {
        script {
          sh "mkdir out || true"
          sh "bandit -r -f html -o out/bandit.html -f xml -o out/junit.xml ."

          publishHTML([
            allowMissing: false,
            alwaysLinkToLastBuild: false,
            keepAll: true,
            reportDir: "./out/",
            reportFiles: 'bandit.html',
            includes: '**/*',
            reportName: 'Ansible CMDB Report',
            reportTitles: "Ansible CMDB Report Index"
          ])

          junit "out/junit.xml"

        }
      }
    }
    stage('SonarQube analysis') {
      environment {
        SONAR_USER_HOME = "$WORKSPACE"
      }
      steps {
        script {
          withSonarQubeWrapper(verbose: true, skipMaven: true, project: "NABLA", repository: "nabla-hooks") {

          }
        }
      } // steps
    } // stage SonarQube analysis
  }
  post {
    always {
      archiveArtifacts artifacts: "**/*.log", onlyIfSuccessful: false, allowEmptyArchive: true
      runHtmlPublishers(["LogParserPublisher", "AnalysisPublisher"])
    }
    success {
      script {
        if (! isReleaseBranch()) { cleanWs() }
      }
    }
  } // post
}
