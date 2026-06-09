root@srv2:~/devops-enterprise-lab# vi  Jenkinsfile
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
  
