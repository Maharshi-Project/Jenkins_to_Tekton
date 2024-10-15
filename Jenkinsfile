pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'myapp:${BUILD_NUMBER}'
        DOCKER_REGISTRY = 'docker.example.com'
        KUBE_CONFIG = credentials('kubeconfig')
    }

    options {
        timeout(time: 1, unit: 'HOURS')
        disableConcurrentBuilds()
        ansiColor('xterm')
    }

    triggers {
        pollSCM('H/15 * * * *')
        cron('@daily')
    }

    parameters {
        string(name: 'DEPLOY_ENV', defaultValue: 'staging', description: 'Deployment environment')
        booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Run tests?')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'mvn clean package -DskipTests'
            }
        }

        stage('Unit Tests') {
            when {
                expression { params.RUN_TESTS }
            }
            steps {
                sh 'mvn test'
            }
            post {
                always {
                    junit '**/target/surefire-reports/*.xml'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh 'mvn sonar:sonar'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-credentials') {
                        docker.image("${DOCKER_IMAGE}").push()
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            when {
                expression { params.DEPLOY_ENV == 'staging' || params.DEPLOY_ENV == 'production' }
            }
            steps {
                script {
                    withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                        sh """
                            kubectl --kubeconfig=\$KUBECONFIG apply -f k8s/deployment.yaml
                            kubectl --kubeconfig=\$KUBECONFIG set image deployment/myapp myapp=${DOCKER_REGISTRY}/${DOCKER_IMAGE}
                        """
                    }
                }
            }
        }

        stage('Integration Tests') {
            when {
                expression { params.RUN_TESTS && params.DEPLOY_ENV == 'staging' }
            }
            steps {
                sh 'mvn verify -Pintegration-tests'
            }
        }

        stage('Performance Tests') {
            when {
                expression { params.DEPLOY_ENV == 'staging' }
            }
            steps {
                sh 'jmeter -n -t performance_tests.jmx -l results.jtl'
            }
            post {
                always {
                    perfReport 'results.jtl'
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'target/*.jar', fingerprint: true
            cleanWs()
        }
        success {
            slackSend channel: '#ci-cd', color: 'good', message: "Build Successful: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
        }
        failure {
            slackSend channel: '#ci-cd', color: 'danger', message: "Build Failed: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
            emailext subject: "Build Failed: ${env.JOB_NAME} ${env.BUILD_NUMBER}",
                      body: 'Check console output at ${env.BUILD_URL}',
                      to: 'team@example.com'
        }
    }
}