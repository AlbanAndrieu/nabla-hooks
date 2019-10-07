#!/usr/bin/env groovy
@Library('jenkins-pipeline-scripts') _

def DOCKER_REGISTRY="docker.hub"
def DOCKER_ORGANISATION="nabla"
def DOCKER_TAG="latest"
def DOCKER_NAME="ansible-jenkins-slave"

def DOCKER_REGISTRY_URL="https://${DOCKER_REGISTRY}"
def DOCKER_REGISTRY_CREDENTIAL='jenkins'
def DOCKER_IMAGE="${DOCKER_REGISTRY}/${DOCKER_ORGANISATION}/${DOCKER_NAME}:${DOCKER_TAG}"

def DOCKER_OPTS_ROOT = [
    '-v /etc/passwd:/etc/passwd:ro',
    '-v /etc/group:/etc/group:ro',
].join(" ")

def DOCKER_OPTS_BASIC = [
    '--dns-search=nabla.mobi',
    '-v /usr/local/sonar-build-wrapper:/usr/local/sonar-build-wrapper',
    '-v /workspace/slave/tools/:/workspace/slave/tools/',
    '-v /jenkins:/home/jenkins',
    DOCKER_OPTS_ROOT,
    '--entrypoint=\'\'',
].join(" ")

def DOCKER_OPTS_COMPOSE = [
    DOCKER_OPTS_BASIC,
    '-v /var/run/docker.sock:/var/run/docker.sock',
].join(" ")

pipeline {
  agent none
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
    //skipStagesAfterUnstable()
    parallelsAlwaysFailFast()
    ansiColor('xterm')
    timeout(time: 60, unit: 'MINUTES')
    timestamps()
  }
  stages {
    stage('Setup') {
      agent {
        docker {
          image DOCKER_IMAGE
          alwaysPull true
          reuseNode true
          registryUrl DOCKER_REGISTRY_URL
          registryCredentialsId DOCKER_REGISTRY_CREDENTIAL
          args DOCKER_OPTS_COMPOSE
          label 'docker-compose'
        }
      }
      steps {
        script {
          properties(createPropertyList())
          setBuildName()
          if (! isReleaseBranch()) { abortPreviousRunningBuilds() }
        }
      }
    }
    stage('Documentation') {
      agent {
        docker {
          image DOCKER_IMAGE
          alwaysPull true
          reuseNode true
          registryUrl DOCKER_REGISTRY_URL
          registryCredentialsId DOCKER_REGISTRY_CREDENTIAL
          args DOCKER_OPTS_COMPOSE
          label 'docker-compose'
        }
      }
      // Creates documentation using Sphinx and publishes it on Jenkins
      // Copy of the documentation is rsynced
      steps {
        script {

          def shell = "#!/bin/bash \n" +
                  "../scripts/run-python.sh \n" +
                  "./build.sh"

          runSphinx(shell: shell, targetDirectory: "nabla-hooks/")

          recordIssues enabledForFailure: true, tool: sphinxBuild()
        }
      }
    }
    stage('Build') {
      agent {
        docker {
          image DOCKER_IMAGE
          alwaysPull true
          reuseNode true
          registryUrl DOCKER_REGISTRY_URL
          registryCredentialsId DOCKER_REGISTRY_CREDENTIAL
          args DOCKER_OPTS_COMPOSE
          label 'docker-compose'
        }
      }
      environment {
        SONAR_USER_HOME = "$WORKSPACE"
      }
      steps {
        script {
          try {

            tee("python.log") {
                sh "#!/bin/bash \n" +
                  "whoami \n" +
                  "./scripts/run-python.sh"
            } // tee

            tee("tox.log") {
                sh "#!/bin/bash \n" +
                  "./build.sh"
            } // tee

            publishHTML([
              allowMissing: true,
              alwaysLinkToLastBuild: false,
              keepAll: true,
              reportDir: "./output/htmlcov/",
              reportFiles: 'index.html',
              includes: '**/*',
              reportName: 'Coverage Report',
              reportTitles: "Coverage Report Index"
            ])

            withSonarQubeWrapper(verbose: true, skipMaven: true, project: "NABLA", repository: "nabla-hooks") {

            }

          } catch (e) {
            currentBuild.result = 'FAILURE'
            build = "FAIL" // make sure other exceptions are recorded as failure too
            throw e
          } finally {
            archiveArtifacts artifacts: "*.log", onlyIfSuccessful: false, allowEmptyArchive: true

            runHtmlPublishers(["LogParserPublisher", "AnalysisPublisher"])

            //recordIssues enabledForFailure: true, tool: [flake8(), pyLint()]
            //pep8()
            //yamlLint()
          }

        }
      } // steps
    } // stage SonarQube analysis
    stage("Bandit Report") {
      agent {
        docker {
          image DOCKER_IMAGE
          alwaysPull true
          reuseNode true
          registryUrl DOCKER_REGISTRY_URL
          registryCredentialsId DOCKER_REGISTRY_CREDENTIAL
          args DOCKER_OPTS_COMPOSE
          label 'docker-compose'
        }
      }
      when {
        expression { BRANCH_NAME ==~ /(release|master|develop)/ }
      }
      steps {
        script {
          try {
            tee("bandit.log") {
              sh "./test/bandit.sh"

              publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: false,
                keepAll: true,
                reportDir: "./output/",
                reportFiles: 'bandit.html',
                includes: '**/*',
                reportName: 'Bandit Report',
                reportTitles: "Bandit Report Index"
              ])

              junit testResults: 'output/junit.xml', healthScaleFactor: 2.0, allowEmptyResults: true, keepLongStdio: true
            } // tee

          } catch (e) {
            currentBuild.result = 'FAILURE'
            build = "FAIL" // make sure other exceptions are recorded as failure too
            throw e
          } finally {
            archiveArtifacts artifacts: "bandit.log", onlyIfSuccessful: false, allowEmptyArchive: true

            //recordIssues enabledForFailure: true, tool: [flake8(), pyLint()]
            //pep8()
            //yamlLint()
          }
        }
      }
    }
  }
  post {
    cleanup {
      wrapCleanWs(isEmailEnabled: false)
    } // cleanup
  } // post
}
