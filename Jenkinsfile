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
        stage('IncludeOS-Build') {
            steps {
                script {
                  sh '''
                  . ./etc/use_clang_version.sh
                  git pull https://github.com/hioa-cs/IncludeOS.git dev
                  '''
                  try {
                    sh '''
                      ./install.sh -y
                      int buildDuration = ${currentBuild.duration}
                      echo "TimeTaken to BUILD IncludeOS: $buildDuration ms"
                    '''
                  } catch(e) {
                    test_ok = false
                    echo e.toString()
                  }

                  if(test_ok) {
                    currentBuild.result = "SUCCESS"
                  }
                  else {
                    currentBuild.result = "FAILURE"
                  }


                }
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
                script {
                  sh '''
                  chmod u+w ~
                  . ./etc/use_clang_version.sh
                  cd test
                  '''
                  try {
                    python testrunner.py -s intrusive stress misc -p 1 -S
                  } catch(e) {
                    test_ok = false
                    echo e.toString()
                  }

                  if(test_ok) {
                    currentBuild.result = "SUCCESS"
                  }
                  else {
                    currentBuild.result = "FAILURE"
                  }
                }
            }
        }
        stage('Service-Tests') {
            steps {
                script {
                  sh '''
                  chmod u+w ~
                  . ./etc/use_clang_version.sh
                  cd test
                  '''
                  try {
                    python testrunner.py -t misc -p 1 -S
                  } catch(e) {
                    test_ok = false
                    echo e.toString()
                  }

                  if(test_ok) {
                    currentBuild.result = "SUCCESS"
                  }
                  else {
                    currentBuild.result = "FAILURE"
                  }
                }
            }
        }
        stage('Stress-Tests') {
            steps {
                script {
                  sh '''
                  chmod u+w ~
                  . ./etc/use_clang_version.sh
                  cd test
                  '''
                  try {
                    python testrunner.py -s stress -p 1 -S
                  } catch(e) {
                    test_ok = false
                    echo e.toString()
                  }

                  if(test_ok) {
                    currentBuild.result = "SUCCESS"
                  }
                  else {
                    currentBuild.result = "FAILURE"
                  }
                }
            }
        }
      }
      post {
        success {
          slackSend (color: '#00FF00', channel: '#devops', message: "*IncludeOS Build-Test SUCCESSFUL:* Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (<${env.RUN_DISPLAY_URL}|Open>) Stats: available on Internal Stats page.")
        }

        failure {
          slackSend (color: '#FF0000', channel: '#devops', message: "*IncludeOS Build-Test FAILED:* Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (<${env.RUN_DISPLAY_URL}|Open>) Stats: available on Internal Stats page")
        }

        aborted {
          slackSend (color: '#edba02', channel: '#devops', message: "*IncludeOS Build-Test ABORTED:* Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (<${env.RUN_DISPLAY_URL}|Open>) Stats: available on Internal Stats page")
        }

      }
}
