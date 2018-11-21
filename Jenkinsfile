pipeline {
    agent {
      node {
        label 'os_includeosbuilder'
      }
    }

    environment {
      INCLUDEOS_PREFIX = "${env.WORKSPACE + '/IncludeOS_install'}"
      INCLUDEOS_ENABLE_TEST = "ON"
      num_jobs = "-j 8"
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '100'))
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                sh './install.sh -y'
            }
        }
        stage('Stat-Configs') {
            steps {
                echo 'configuring ..'
                sh 'cp ~/config/* $(pwd)/test/'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
                sh '''
                cd test
                ./testrunner.py -s intrusive misc net stress -p 1
                '''
            }
        }
        stage('Build-Misc') {
            steps {
                echo 'Deploying Services....'
                sh '''
                cd test
                ./testrunner.py -s intrusive -t misc -p 1
                '''
            }
        }

        stage('Stress Test') {
            steps {
                echo 'Stress Testing ...'
                sh '''
                cd test
                ./testrunner.py -s intrusive -t stress -p 1
                '''
            }
        }
    }
    post {
      success {
        slackSend (color: '#00FF00', channel: '#devops', message: "SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
      }

      failure {
        slackSend (color: '#FF0000', channel: '#devops', message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
      }
    }
}
