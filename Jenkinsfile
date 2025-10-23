pipeline {
    agent any

    environment {
        IMAGE_NAME = "karathcode/devops-a2-streamlit-app"
    }

    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'github-creds-college', git branch: 'main', url: 'https://github.com/Karath-Vamsi/DevOps-Assignment-2.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}:latest")
                }
            }
        }

        stage('Run Container') {
            steps {
                script {
                    sh "docker run -d -p 8501:8501 ${IMAGE_NAME}:latest"
                }
            }
        }
    }
}
