pipeline {
    agent any

    environment {
        IMAGE_NAME    = "api-service"
        IMAGE_TAG     = "0.1.${env.BUILD_NUMBER}"
        K8S_NAMESPACE = "devops-sre-lab"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Unit tests / Lint (simulado)') {
            steps {
                sh '''
                echo "[INFO] Aquí normalmente correría tests y lint de la app FastAPI"
                echo "[INFO] Por ejemplo: pytest, mypy, flake8, etc."
                '''
            }
        }

        stage('Build Docker image (simulado)') {
            steps {
                sh '''
                echo "[INFO] Aquí normalmente haría el build de la imagen Docker"
                echo "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} apps/api-service"
                '''
            }
        }

        stage('Push image to registry (simulado)') {
            steps {
                sh '''
                echo "[INFO] Aquí haría login al registry y push de la imagen"
                echo "docker push <registry>/${IMAGE_NAME}:${IMAGE_TAG}"
                '''
            }
        }

        stage('Deploy to Kubernetes (GitOps style, simulado)') {
            steps {
                sh '''
                echo "[INFO] Aquí normalmente actualizaría el manifiesto de k8s con la nueva imagen"
                echo "sed -i 's/image: api-service:.*/image: api-service:${IMAGE_TAG}/' k8s/base/api-service/deployment.yaml"
                echo "[INFO] Y luego ArgoCD/GitOps se encargaría de sincronizar con el cluster"
                '''
            }
        }
    }

    post {
        always {
            echo "[INFO] Pipeline finished with status: ${currentBuild.currentResult}"
        }
    }
}
