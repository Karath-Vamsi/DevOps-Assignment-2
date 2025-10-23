pipeline {
    agent any

    environment {
        IMAGE_NAME = "karathcode/devops-a2-streamlit-app"
        IMAGE_TAG = "latest"
        DOCKER_CREDENTIALS = "dockerhub-creds" // Jenkins Docker Hub credentials ID
        GITHUB_CREDENTIALS = "github-creds-college"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', credentialsId: "${GITHUB_CREDENTIALS}", url: 'https://github.com/Karath-Vamsi/DevOps-Assignment-2.git'
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat """
                        echo Logging into Docker Hub...
                        docker logout
                        docker login -u %DOCKER_USER% -p %DOCKER_PASS%
                    """
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                bat "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                bat """
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat """
                    echo Checking Kubernetes status...
                    kubectl config current-context
                    echo Deploying to cluster...
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                """
            }
        }

        stage('Cleanup Old Containers') {
            steps {
                bat """
                    echo Cleaning up old containers...
                    docker container prune -f
                    docker image prune -f
                """
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
