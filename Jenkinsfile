pipeline{
    agent any
    environment {
        DOCKER_IMAGE_NAME = 'calculator'
        GITHUB_REPO_URL = 'https://github.com/abhisheksharma402/SPE-Mini-Project.git'
    }
    stages{
        stage('Clone Project'){
            steps {
                script{
                    git branch: 'main', url: "${GITHUB_REPO_URL}"
                }
            }
        }
        stage('Maven Build'){
            steps {
                sh 'mvn clean install -DskipTests'
            }
        }
        stage('Testing'){
            steps {
                sh 'mvn test'
            }
        }
        stage('Building Docker Image')
        {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE_NAME}", '.')
                }
            }
        }
        stage('Pushing Docker Image')
        {
            steps {
                script {
                    docker.withRegistry('', 'dockerhub-credentials') {
                        sh "docker image tag calculator abhisheksharma402/calculator:version2.0"
                        sh "docker push abhisheksharma402/calculator:version2.0"
                    }
                }
            }
        }
        stage('Run Ansible Inventory and Playbook'){
            steps {
                script {
                    ansiblePlaybook (
                        playbook: 'playbook.yml',
                        inventory: 'inventory'
                    )
                }
            }
        }
    }
}