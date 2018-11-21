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
        stage('Test') {
            steps {
                echo 'Testing..'
                sh '''
                cp ~/config/* test/
                cd test
                ./testrunner.py -s intrusive misc net stress
                '''
            }
        }
        stage('Build-Misc') {
            steps {
                echo 'Deploying Services....'
                sh '''
                cd test
                ./testrunner.py -s intrusive -t misc
                '''
            }
        }

        stage('Stress Test') {
            steps {
                echo 'Stress Testing ...'
                sh '''
                cd test
                ./testrunner.py -s intrusive -t stress
                '''
            }
        }
    }
/*    post {
        always {
	    /* slackNotifier - current build result as parameter */
            slackNotifier
            cleanWs()
        }
    } */
}
