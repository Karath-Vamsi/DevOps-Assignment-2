<!-- # DevOps Assignment 2: Streamlit App Deployment with Jenkins, Docker & Kubernetes

## Project Overview

This project demonstrates a complete CI/CD pipeline for deploying a Streamlit application using Jenkins, Docker, and Kubernetes. The automation covers:

- Cloning the repository from GitHub
- Building a Docker image of the Streamlit app
- Pushing the image to Docker Hub
- Deploying the app to a Kubernetes cluster
- Optionally opening the app locally via port-forwarding

DevOps-Assignment-2/
├── Dockerfile
├── Jenkinsfile
├── requirements.txt
├── src/
│   └── app.py (Streamlit application code)
├── k8/
│   ├── deployment.yaml (Kubernetes Deployment manifest)
│   └── service.yaml (Kubernetes Service manifest)
└── README.md


## Prerequisites

- Jenkins installed and configured
- Docker installed and running
- Kubernetes cluster available (minikube, kind, or cloud)
- kubectl configured to access the cluster
- GitHub repository with Jenkins credentials
- Docker Hub account for pushing images

## Pipeline Steps

### 1. Checkout SCM (GitHub repository)
**Command used internally by Jenkins:**
```bash
git checkout <branch> using stored credentials
```

### 2. Docker Login
**Command:**
```bash
docker login -u <dockerhub-username> -p <docker-password>
```
**Description:** Uses Jenkins credentials to authenticate securely  

### 3. Build Docker Image
**Command:**
```bash
docker build -t <dockerhub-username>/devops-a2-streamlit-app:latest .
```

**Dockerfile details:**
- Base image: `python:3.10-slim`
- Install dependencies from `requirements.txt`
- Copy app source code
- Expose port `8501`
- Command to run app: `streamlit run src/app.py --server.port=8501 --server.address=0.0.0.0`


### 4. Push Docker Image to Docker Hub
**Command:**
```bash
docker push <dockerhub-username>/devops-a2-streamlit-app:latest
```
**Description:** Jenkins securely passes credentials  

### 5. Deploy to Kubernetes
**Apply Deployment manifest:**
```bash
kubectl --kubeconfig <kubeconfig-file> apply -f k8/deployment.yaml
```

**Apply Service manifest:**
```bash
kubectl --kubeconfig <kubeconfig-file> apply -f k8/service.yaml
```

**Deployment.yaml:**
- Deployment with 1 replica
- Container image from Docker Hub
- Container port 8501

**Service.yaml:**
- NodePort service
- Target port 8501
- Node port 30001


### 6. Cleanup Old Containers (Optional)
- Skipped in current setup
- Can use `docker ps` and `docker rm` to remove old containers

### 7. Open App Locally (Optional)
**Command for port-forwarding:**
```bash
kubectl port-forward service/streamlit-service 8501:8501
```
**Open browser:** `http://localhost:8501`   -->



# DevOps Assignment 2: Streamlit App Deployment with Jenkins, Docker & Kubernetes

## Project Overview

This project demonstrates a complete CI/CD pipeline for deploying a Streamlit application using Jenkins, Docker, and Kubernetes. The automation covers:

- Cloning the repository from GitHub
- Building a Docker image of the Streamlit app
- Pushing the image to Docker Hub
- Deploying the app to a Kubernetes cluster
- Optionally opening the app locally via port-forwarding

## Repository Structure

```
DevOps-Assignment-2/
├── Dockerfile
├── Jenkinsfile
├── requirements.txt
├── src/
│   └── app.py (Streamlit application code)
├── k8/
│   ├── deployment.yaml (Kubernetes Deployment manifest)
│   └── service.yaml (Kubernetes Service manifest)
└── README.md
```

## Prerequisites

- Jenkins installed and configured
- Docker installed and running
- Kubernetes cluster available (minikube, kind, or cloud)
- kubectl configured to access the cluster
- GitHub repository with Jenkins credentials
- Docker Hub account for pushing images

## Pipeline Steps with Commands

### Checkout SCM (GitHub repository)

**Jenkinsfile stage:**
```groovy
stage('Checkout SCM') {
    steps {
        checkout([$class: 'GitSCM', branches: [[name: '*/main']],
                  userRemoteConfigs: [[url: 'https://github.com/Karath-Vamsi/DevOps-Assignment-2.git',
                                       credentialsId: 'github-creds-college']]])
    }
}
```

**Terminal equivalent:**
```bash
git clone https://github.com/Karath-Vamsi/DevOps-Assignment-2.git
git checkout main
```

### Docker Login

**Jenkinsfile stage:**
```groovy
stage('Docker Login') {
    withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
        bat "docker logout"
        bat "docker login -u %DOCKER_USER% -p %DOCKER_PASS%"
    }
}
```

**Terminal equivalent:**
```bash
docker logout
docker login -u <dockerhub-username> -p <docker-password>
```

### Build Docker Image

**Jenkinsfile stage:**
```groovy
stage('Build Docker Image') {
    steps {
        bat 'docker build -t karathcode/devops-a2-streamlit-app:latest .'
    }
}
```

**Terminal equivalent:**
```bash
docker build -t karathcode/devops-a2-streamlit-app:latest .
```

**Dockerfile contents:**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Push Docker Image to Docker Hub

**Jenkinsfile stage:**
```groovy
stage('Push to Docker Hub') {
    steps {
        bat 'docker push karathcode/devops-a2-streamlit-app:latest'
    }
}
```

**Terminal equivalent:**
```bash
docker push karathcode/devops-a2-streamlit-app:latest
```

### Deploy to Kubernetes

**Jenkinsfile stage:**
```groovy
stage('Deploy to Kubernetes') {
    withCredentials([file(credentialsId: 'kubeconfig-file', variable: 'KUBECONFIG_FILE')]) {
        bat 'kubectl --kubeconfig %KUBECONFIG_FILE% apply -f k8/deployment.yaml'
        bat 'kubectl --kubeconfig %KUBECONFIG_FILE% apply -f k8/service.yaml'
    }
}
```

**Terminal equivalent:**
```bash
kubectl --kubeconfig <kubeconfig-file> apply -f k8/deployment.yaml
kubectl --kubeconfig <kubeconfig-file> apply -f k8/service.yaml
```

**deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: streamlit-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: streamlit
  template:
    metadata:
      labels:
        app: streamlit
    spec:
      containers:
      - name: streamlit
        image: karathcode/devops-a2-streamlit-app:latest
        ports:
        - containerPort: 8501
```

**service.yaml:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: streamlit-service
spec:
  type: NodePort
  selector:
    app: streamlit
  ports:
    - port: 8501
      targetPort: 8501
      nodePort: 30001
```

### Cleanup Old Containers (Optional)

**Jenkinsfile stage:**
```groovy
stage('Cleanup Old Containers') {
    steps {
        echo 'Skipping cleanup for now...'
    }
}
```

**Terminal equivalent (optional):**
```bash
docker ps
docker rm <container-id>
```

### Open App Locally (Optional)

**Jenkinsfile stage:**
```groovy
stage('Open App Locally') {
    steps {
        withCredentials([file(credentialsId: 'kubeconfig-file', variable: 'KUBECONFIG_FILE')]) {
            bat 'start cmd /c "kubectl --kubeconfig %KUBECONFIG_FILE% port-forward service/streamlit-service 8501:8501 & timeout /t 5 & start http://localhost:8501"'
        }
    }
}
```

**Terminal equivalent:**
```bash
kubectl port-forward service/streamlit-service 8501:8501
# Open browser at http://localhost:8501
```

## Notes

- NodePort (30001) may conflict with other services; port-forwarding is recommended for local development.
- Jenkins automates Docker build, push, and Kubernetes deployment.
- Docker Hub credentials are stored securely in Jenkins.
- Kubernetes manifests can be modified for scaling, resource limits, or environment variables.
```