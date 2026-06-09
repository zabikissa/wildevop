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

                container('python') {
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
        }

        stage('Build Docker') {
            steps {
                echo "🐳 Building Docker image"

                container('docker') {
                    sh "docker build -t ${IMAGE} ."
                }
            }
        }

        stage('Scan Security (Trivy)') {
            steps {
                echo "🔍 Security scan"

                container('docker') {
                    sh "trivy image ${IMAGE} || true"
                }
            }
        }

        stage('Push Registry') {
            steps {
                echo "📦 Push image"

                container('docker') {
                    sh """
                        docker tag ${IMAGE} ${REGISTRY}/${IMAGE}
                        docker push ${REGISTRY}/${IMAGE}
                    """
                }
            }
        }

        stage('Deploy Kubernetes') {
            steps {
                echo "☸️ Deploy to Kubernetes"

                container('docker') {
                    sh "kubectl apply -f k8s/"
                }
            }
        }
    }

    post {
        success {
            echo "✅ PIPELINE SUCCESS"
        }
        failure {
            echo "❌ PIPELINE FAILED - check logs"
        }
    }
}
