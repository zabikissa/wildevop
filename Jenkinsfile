pipeline {
    agent any

    environment {
        IMAGE = "devops-api:latest"
        REGISTRY = "localhost:5000"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "📥 Checkout code"
                checkout scm
            }
        }

        stage('Test') {
            steps {
                echo "🧪 Running tests"

                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest
                    pytest -v
                '''
            }
        }

        stage('Build Docker') {
            steps {
                echo "🐳 Building Docker image"
                sh "docker build -t ${IMAGE} ."
            }
        }

        stage('Scan Security (Trivy)') {
            steps {
                echo "🔍 Security scan"
                sh "trivy image ${IMAGE} || true"
            }
        }

        stage('Push Registry') {
            steps {
                echo "📦 Push image"

                sh '''
                    docker tag devops-api:latest localhost:5000/devops-api:latest
                    docker push localhost:5000/devops-api:latest
                '''
            }
        }

        stage('Deploy Kubernetes') {
            steps {
                echo "☸️ Deploy to Kubernetes"
                sh "kubectl apply -f k8s/"
            }
        }
    }

    post {
        success {
            echo "✅ PIPELINE SUCCESS"
        }
        failure {
            echo "❌ PIPELINE FAILED"
        }
    }
}
