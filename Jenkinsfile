def artifactory_name = "kristianj"
def artifactory_repo = "includeos-develop"
def repo_url = 'https://github.com/staiyeba/IncludeOS.git'
def repo_branch = 'taiyeba-conan'
node {
   def server
   def client
   def serverName
stage("Get project"){
    git branch: repo_branch, url: repo_url
}
stage("Configure Artifactory/Conan"){
    server = Artifactory.server includeos-develop
    client = Artifactory.newConanClient()
    serverName = client.remote.add server: server, repo: artifactory_repo
}
stage("Get dependencies and publish build info"){
    sh "mkdir -p build"
    dir ('build') {
      def b = client.run(command: "cmake -DCONAN_PROFILE=clang-6.0 ../")
      server.publishBuildInfo b
    }
}
    stage("Build/Test project"){
        dir ('build') {
          sh "make ../ && make install ../"
        }
    }
}
