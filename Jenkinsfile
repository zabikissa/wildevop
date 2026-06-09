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

        stage('Test (Docker isolated)') {
            steps {
                echo "🧪 Running tests inside Docker"

                sh '''
                    docker run --rm \
                    -v $PWD:/app \
                    -w /app \
                    python:3.11 \
                    bash -c "pip install --upgrade pip && pip install -r requirements.txt && pip install pytest && pytest -v"
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
                    docker tag ${IMAGE} ${REGISTRY}/${IMAGE}
                    docker push ${REGISTRY}/${IMAGE}
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
