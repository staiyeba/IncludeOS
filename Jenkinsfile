pipeline {
  agent { label 'vaskemaskin' }

  environment {
    PROFILE_x86_64 = 'clang-6.0-linux-x86_64'
    PROFILE_x86 = 'clang-6.0-linux-x86'
    CPUS = """${sh(returnStdout: true, script: 'nproc')}"""
    INCLUDEOS_PREFIX = "${env.WORKSPACE}/install"
    CC = 'clang-6.0'
    CXX = 'clang++-6.0'
    USER = 'includeos'
    CHAN = 'test'
    MOD_VER= '0.13.0'
    REMOTE = 'includeos-test'
    COVERAGE_DIR = "${env.COVERAGE_DIR}/${env.JOB_NAME}"
  }

  stages {
    stage('Setup') {
      steps {
        sh 'mkdir -p install'
        sh 'cp conan/profiles/* ~/.conan/profiles/'
        sh 'printenv'
      }
    }

    stage('Pull Request pipeline') {
      stages {
        /* TODO
        stage('build chainloader 32bit') {
          steps {
        sh """
              cd src/chainload
            rm -rf build || :&& mkdir build
            cd build
            conan link .. chainloader/$MOD_VER@$USER/$CHAN --layout=../layout.txt
            conan install .. -pr $PROFILE_x86 -u
            cmake --build . --config Release
        """
          }
        }
        */
        stage('Code coverage') {
          steps {
            sh script: "mkdir -p coverage; rm -r $COVERAGE_DIR || :", label: "Setup"
            sh script: "cd coverage; env CC=gcc CXX=g++ cmake -DCOVERAGE=ON -DCODECOV_HTMLOUTPUTDIR=$COVERAGE_DIR ../test", label: "Cmake"
            sh script: "cd coverage; make -j $CPUS", label: "Make"
            sh script: "cd coverage; make coverage", label: "Make coverage"
            echo "code coverage in file: $COVERAGE_DIR"
            echo "Code coverage in: http://vaskemaskin.includeos.org:8080/coverage_includeos/${env.JOB_NAME}"
          }
          post {
            success {
              script {
                if (env.CHANGE_ID) {
                  pullRequest.comment("Code coverage: http://vaskemaskin.includeos.org:8080/coverage_includeos/${env.JOB_NAME}")
                }
              }
            }
          }
        }
      }
    }

    stage('Dev branch pipeline') {
      when {
        anyOf {
          branch 'master'
          branch 'dev'
        }
      }
      stages {
        stage('Build Conan package') {
          steps {
            build_conan_package("$PROFILE_x86", "ON")
            build_conan_package("$PROFILE_x86_64")
          }
        }
        stage('Upload to bintray') {
          steps {
            script {
              def version = sh (
                script: 'conan inspect -a version . | cut -d " " -f 2',
                returnStdout: true
              ).trim()
              sh script: "conan upload --all -r $REMOTE includeos/${version}@$USER/$CHAN", label: "Upload to bintray"
            }
          }
        }
      }
    }
  }
}

def build_editable(String location, String name) {
  sh """
    cd $location
    mkdir -p build
    cd build
    conan link .. $name/$MOD_VER@$USER/$CHAN --layout=../layout.txt
    conan install .. -pr $PROFILE_x86_64 -u
    cmake -DARCH=x86_64 ..
    cmake --build . --config Release
  """
}

def build_conan_package(String profile, basic="OFF") {
  sh script: "conan create . $USER/$CHAN -pr ${profile} -o basic=${basic}", label: "Build with profile: $profile"
}
