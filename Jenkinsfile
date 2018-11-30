pipeline {
    agent {
      node {
        label 'jenkins_includeos'
      }
    }

    environment {
      INCLUDEOS_SRC = "${env.WORKSPACE}"
      INCLUDEOS_PREFIX = "${env.WORKSPACE + '/IncludeOS_install'}"
      INCLUDEOS_ENABLE_TEST = "ON"
      INCLUDEOS_ENABLE_LXP = "ON"
      num_jobs = "-j 8"

    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
        timestamps()
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                sh '''
                . ./etc/use_clang_version.sh
                git pull https://github.com/hioa-cs/IncludeOS.git dev
                ./install.sh -y
                '''
            }
        }
        stage('Integration-Tests') {
            steps {
                echo 'Testing..'
                sh '''
                chmod u+w ~
                . ./etc/use_clang_version.sh
                cd test
                withCredentials([file(credentialsId: 'solid-feat', variable: 'cilent_secret')]) {
                  set +x
                }
                withCredentials([file(credentialsId: 'oauth2client', variable: 'access_token')]) {
                  set +x
                }
                python testrunner.py -s intrusive stress misc -p 1 -S
                '''
            }
        }
        stage('Service-Tests') {
            steps {
                echo 'Testing..'
                sh '''
                chmod u+w ~
                . ./etc/use_clang_version.sh
                cd test
                python testrunner.py -t misc -p 1 -S
                '''
            }
        }
        stage('Stress-Test') {
            steps {
                echo 'Testing..'
                sh '''
                chmod u+w ~
                . ./etc/use_clang_version.sh
                cd test
                python testrunner.py -s stress -p 1 -S
                '''
            }
        }

    }
    post {
      success {
        slackSend (color: '#00FF00', channel: '#devops', message: "SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL}) Stats: available on Internal Stats page.")
      }

      failure {
        slackSend (color: '#FF0000', channel: '#devops', message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL}) Stats: available on Internal Stats page")
      }
    }
}
