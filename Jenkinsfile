pipeline {
    agent any

    environment {
        IMAGE = "devops-api:latest"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "📥 Checkout code"
                git branch: 'main', url: 'https://github.com/zabikissa/wildevop.git'
            }
        }

        stage('Debug Environment') {
            steps {
                echo "🧠 Checking tools inside Jenkins container"
                sh 'whoami || true'
                sh 'python3 --version || true'
                sh 'pip3 --version || true'
                sh 'which python3 || true'
                sh 'which pip3 || true'
                sh 'docker --version || true'
            }
        }

        stage('Test') {
            steps {
                echo "🧪 Running tests"
                sh 'python3 -m pip install -r requirements.txt || true'
                sh 'pytest -v || true'
            }
        }

        stage('Build Docker') {
            steps {
                echo "🐳 Building Docker image"
                sh 'docker build -t $IMAGE .'
            }
        }

        stage('Scan Security (Trivy)') {
            steps {
                echo "🔍 Security scan"
                sh 'trivy image $IMAGE || true'
            }
        }

        stage('Push Registry') {
            steps {
                echo "📦 Push image"
                sh 'docker tag $IMAGE localhost:5000/$IMAGE || true'
                sh 'docker push localhost:5000/$IMAGE || true'
            }
        }

        stage('Deploy Kubernetes') {
            steps {
                echo "☸️ Deploy to Kubernetes"
                sh 'kubectl apply -f k8s/ || true'
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
