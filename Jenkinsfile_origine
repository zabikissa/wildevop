pipeline {
    agent any

    environment {
        IMAGE = "devops-api:latest"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/zabikissa/wildevop.git'
            }
        }

        stage('Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pytest -v'
            }
        }

        stage('Build Docker') {
            steps {
                sh 'docker build -t $IMAGE .'
            }
        }

        stage('Scan Security (Trivy)') {
            steps {
                sh 'trivy image $IMAGE || true'
            }
        }

        stage('Push Registry') {
            steps {
                sh 'docker tag $IMAGE localhost:5000/$IMAGE'
                sh 'docker push localhost:5000/$IMAGE'
            }
        }

        stage('Deploy Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s/'
            }
        }
    }
}

