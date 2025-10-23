pipeline {
    agent any

    environment {
        IMAGE_NAME = "karathcode/devops-a2-streamlit-app"
        IMAGE_TAG = "latest"
        DOCKER_CREDENTIALS = "dockerhub-creds" // Jenkins Docker Hub credentials ID
        GITHUB_CREDENTIALS = "github-creds-college"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', credentialsId: "${GITHUB_CREDENTIALS}", url: 'https://github.com/Karath-Vamsi/DevOps-Assignment-2.git'
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat 'docker logout'
                    bat 'docker login -u %DOCKER_USER% -p %DOCKER_PASS%'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}:${IMAGE_TAG}")
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('', DOCKER_CREDENTIALS) {
                        docker.image("${IMAGE_NAME}:${IMAGE_TAG}").push()
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-file', variable: 'KUBECONFIG_FILE')]) {
                    bat 'kubectl --kubeconfig %KUBECONFIG_FILE% apply -f k8/deployment.yaml'
                    bat 'kubectl --kubeconfig %KUBECONFIG_FILE% apply -f k8/service.yaml'
                }
            }
        }

        stage('Cleanup Old Containers') {
            steps {
                echo 'Skipping cleanup for now...'
            }
        }

        stage('Open App Locally') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-file', variable: 'KUBECONFIG_FILE')]) {
                    bat 'start cmd /c "kubectl --kubeconfig %KUBECONFIG_FILE% port-forward service/streamlit-service 8501:8501 & timeout /t 5 & start http://localhost:8501"'
                }
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful!"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
    }
}
