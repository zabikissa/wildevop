pipeline {
    agent any

    environment {
        IMAGE = "wildevop-app:latest"
        REGISTRY = "docker.io/wilfrid"
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
                    python3 -m pip install --upgrade pip
                    python3 -m pip install -r requirements.txt
                    python3 -m pip install pytest

                    PYTHONPATH=. python3 -m pytest -v
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
