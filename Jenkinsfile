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
        timeout(time: 30, unit: 'MINUTES')
	      ansiColor('xterm')
    }

    stages {
        stage('IncludeOS-Build') {
            steps {
                sh '''
                  git clone https://github.com/hioa-cs/IncludeOS.git
                  . ./etc/use_clang_version.sh
                  ./install.sh -y
                '''
                script {
			             echo "TimeTaken to BUILD IncludeOS: ${currentBuild.duration}ms"
                }

                sh 'exit 0'
            }
        }

        stage('Integration-Tests') {
            steps {
              withCredentials([file(credentialsId: 'solid-feat', variable: 'client_secret')]) {
                  sh '''
                    set +x
                    cp $client_secret test/.
                  '''
              }
              withCredentials([file(credentialsId: 'oauth2client', variable: 'access_token')]) {
                  sh '''
                    set +x
                    cp $access_token test/.
                  '''
              }

              sh '''
                chmod u+w ~
                . ./etc/use_clang_version.sh
                cd test

                python testrunner.py -s intrusive stress misc -p 1 -S
              '''
              sh 'exit 0'

            }
        }

        stage('Service-Tests') {
            steps {
                sh '''
                  chmod u+w ~
                  . ./etc/use_clang_version.sh
                  cd test
                  python testrunner.py -t misc -p 1 -S
                '''
                sh 'exit 0'
                }
        }

        stage('Stress-Tests') {
            steps {
                sh '''
                  chmod u+w ~
                  . ./etc/use_clang_version.sh
                  cd test
                  python testrunner.py -t stress -s intrusive -p 1 -S
                '''
                sh 'exit 0'
            }
        }

        stage('Intrusive-Tests') {
            steps {
                sh '''
                  chmod u+w ~
                  . ./etc/use_clang_version.sh
                  cd test
                  python testrunner.py -t intrusive -p 1 -S
                '''
                sh 'exit 0'
            }
        }

    }

    post {
      success {
        slackSend (color: '#00FF00', channel: '#devops', message: "*IncludeOS Build-Test SUCCESSFUL:* Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (<${env.BUILD_URL}|Open>) Stats: available on Internal Stats page.")
      }

      failure {
        slackSend (color: '#FF0000', channel: '#devops', message: "*IncludeOS Build-Test FAILED:* Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (<${env.BUILD_URL}|Open>) Stats: available on Internal Stats page")
      }

      aborted {
        slackSend (color: '#edba02', channel: '#devops', message: "*IncludeOS Build-Test ABORTED:* Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (<${env.BUILD_URL}|Open>) Stats: available on Internal Stats page")
      }

    }
}
