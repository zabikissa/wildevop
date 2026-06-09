pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:

  - name: python
    image: python:3.11-slim
    command: ['cat']
    tty: true

  - name: docker
    image: docker:24-cli
    command: ['cat']
    tty: true
    volumeMounts:
    - name: docker-sock
      mountPath: /var/run/docker.sock

  volumes:
  - name: docker-sock
    hostPath:
      path: /var/run/docker.sock
"""
        }
    }

    environment {
        IMAGE = "devops-api:latest"
    }

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/zabikissa/wildevop.git'
            }
        }

        stage('Test') {
            steps {
                container('python') {
                    sh '''
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
                container('docker') {
                    sh 'docker build -t $IMAGE .'
                }
            }
        }

        stage('Deploy') {
            steps {
                container('docker') {
                    sh 'kubectl apply -f k8s/'
                }
            }
        }
    }
}
