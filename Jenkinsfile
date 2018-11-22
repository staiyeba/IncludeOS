pipeline {
    agent {
      node {
        label 'os_includeosbuilder'
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
                ./install.sh -y
                '''
            }
        }
        stage('Stat-Configs') {
            steps {
                echo 'configuring ..'
                sh '''
                cp ~/config/* $(pwd)/test/
                ./build_x86_64/unittests/unittests || exit 1
                '''
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
                sh '''
                chmod u+w ~
                . ./etc/use_clang_version.sh
                cd test
                python testrunner.py -s intrusive -p 1
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

export INCLUDEOS_SRC=~/IncludeOS
export INCLUDEOS_PREFIX=~/IncludeOS_install
export CC=clang-5.0
export CXX=clang++-5.0
export num_jobs="-j 8"
export INCLUDEOS_ENABLE_TEST=OFF
