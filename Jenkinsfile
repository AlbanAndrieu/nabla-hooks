#!/usr/bin/env groovy
@Library(value='jenkins-pipeline-scripts@master', changelog=false) _

String DOCKER_REGISTRY_HUB=env.DOCKER_REGISTRY_HUB ?: "index.docker.io/v1".toLowerCase().trim()
String DOCKER_ORGANISATION_HUB="nabla".trim()
String DOCKER_IMAGE_TAG=env.DOCKER_IMAGE_TAG ?: "latest".trim()
//String DOCKER_USERNAME="nabla"
String DOCKER_NAME="ansible-jenkins-slave-docker".trim()

String DOCKER_REGISTRY_HUB_URL=env.DOCKER_REGISTRY_HUB_URL ?: "https://${DOCKER_REGISTRY_HUB}".trim()
String DOCKER_REGISTRY_HUB_CREDENTIAL=env.DOCKER_REGISTRY_HUB_CREDENTIAL ?: "hub-docker-nabla".trim()
String DOCKER_IMAGE="${DOCKER_ORGANISATION_HUB}/${DOCKER_NAME}:${DOCKER_IMAGE_TAG}".trim()

String DOCKER_OPTS_BASIC = getDockerOpts()
String DOCKER_OPTS_COMPOSE = getDockerOpts(isDockerCompose: true, isLocalJenkinsUser: false)

pipeline {
  //agent none
  agent {
    docker {
      image DOCKER_IMAGE
      alwaysPull true
      reuseNode true
      registryUrl DOCKER_REGISTRY_HUB_URL
      registryCredentialsId DOCKER_REGISTRY_HUB_CREDENTIAL
      args DOCKER_OPTS_COMPOSE
      label 'molecule'
    }
  }
  parameters {
    string(name: 'DRY_RUN', defaultValue: '--check', description: 'Default mode used to test playbook')
    booleanParam(name: 'CLEAN_RUN', defaultValue: false, description: 'Clean before run')
  }
  environment {
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
      // Copy of the documentation is rsynced
      steps {
        script {

          def shell = "#!/bin/bash \n" +
                      "pip uninstall ansible \n" +
                      "source ../scripts/run-python.sh \n" +
                      "./build.sh \n"

          runSphinx(shell: shell, targetDirectory: "nabla-hooks/")

          //recordIssues enabledForFailure: true, tool: sphinxBuild()
        }
      }
    }
    stage('Build') {
      environment {
        SONAR_USER_HOME = "$WORKSPACE"
      }
      steps {
        script {
          try {

            tee("python.log") {
              sh "#!/bin/bash \n" +
                 "whoami \n" +
                 "source ./scripts/run-python.sh\n" +
                 "pip uninstall ansible\n" +
                 "pre-commit run -a || true\n" +
                 "./scripts/run-pylint.sh\n" +
                 "./scripts/run-flake8.sh\n"
            } // tee

            tee("build.log") {
                sh "#!/bin/bash \n" +
                   "source ./scripts/run-python.sh\n" +
                   "export TOX_TARGET=\"--notest\"\n" +
                   "./build.sh\n"
            } // tee

            tee("tox.log") {
                sh "#!/bin/bash \n" +
                   "source ./scripts/run-python.sh\n" +
                   "tox\n"
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

            withSonarQubeWrapper(verbose: true,
              skipMaven: true,
              skipSonarCheck: false,
              reportTaskFile: ".scannerwork/report-task.txt",
              isScannerHome: false,
              sonarExecutable: "/usr/local/sonar-runner/bin/sonar-scanner",
              project: "nabla",
              repository: "nabla-hooks")

          } catch (e) {
            currentBuild.result = 'FAILURE'
            build = "FAIL" // make sure other exceptions are recorded as failure too
            throw e
          } finally {
            archiveArtifacts artifacts: "*.log, .tox/py*/log/*.log, output/coverage.xml", onlyIfSuccessful: false, allowEmptyArchive: true

            runHtmlPublishers(["LogParserPublisher", "AnalysisPublisher"])

            //recordIssues enabledForFailure: true, tool: [flake8(), pyLint()]
            //pep8()
            //yamlLint()
          } // finally

        }
      } // steps
    } // stage SonarQube analysis
    stage("Bandit Report") {
      when {
        expression { BRANCH_NAME ==~ /(release|master|develop)/ }
      }
      steps {
        script {
          try {
            tee("bandit.log") {
                sh "#!/bin/bash \n" +
                   "source ./scripts/run-python.sh\n" +
                   "./scripts/run-bandit.sh"

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

              junit testResults: 'output/junit-bandit.xml', healthScaleFactor: 2.0, allowEmptyResults: true, keepLongStdio: true
            } // tee

          } catch (e) {
            currentBuild.result = 'FAILURE'
            build = "FAIL" // make sure other exceptions are recorded as failure too
            throw e
          } finally {
            archiveArtifacts artifacts: "bandit.log, output/junit.xml", onlyIfSuccessful: false, allowEmptyArchive: true

            //recordIssues enabledForFailure: true, tool: [flake8(), pyLint()]
            //pep8()
            //yamlLint()
          }
        }
      }
    }
  } // stages
  post {
    always {
      //recordIssues enabledForFailure: true,
      //  tools: [taskScanner(),
      //          tagList()
      //  ]

      archiveArtifacts allowEmptyArchive: true, artifacts: '*.log. *.json', excludes: null, fingerprint: false, onlyIfSuccessful: false

      //node('any') {
      //  runHtmlPublishers(["LogParserPublisher", "AnalysisPublisher"])
      //}

    } // always
    //cleanup {
    //  wrapCleanWsOnNode(isEmailEnabled: false)
    //} // cleanup
  } // post
}
