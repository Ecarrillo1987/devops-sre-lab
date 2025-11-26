pipeline {
    agent any

    environment {
        IMAGE_NAME   = "api-service"
        IMAGE_TAG    = "0.1.${env.BUILD_NUMBER}"
        REGISTRY     = "docker.io/ECARRILLO1987"  // ajusta a tu usuario real de Docker Hub si quieres
        K8S_NAMESPACE = "devops-sre-lab"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Unit tests / Lint') {
            steps {
                sh '''
                echo "[INFO] Running basic syntax check for FastAPI app"
                python -m compileall apps/api-service/src || exit 1
                '''
            }
        }

        stage('Build Docker image') {
            steps {
                sh '''
                echo "[INFO] Building Docker image ${IMAGE_NAME}:${IMAGE_TAG}"
                docker build -t ${IMAGE_NAME}:${IMAGE_TAG} apps/api-service
                '''
            }
        }

        stage('Push image to registry') {
            when {
                expression { return false } // habilita esto cuando tengas credenciales de Docker Hub
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                                 usernameVariable: 'DOCKER_USER',
                                                 passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                    docker push ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                    '''
                }
            }
        }

        stage('Update k8s manifest (GitOps style)') {
            when {
                expression { return false } // esto es para demo; luego lo puedes habilitar
            }
            steps {
                sh '''
                echo "[INFO] Updating k8s deployment image tag"
                sed -i "s|image: api-service:.*|image: ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}|" k8s/base/api-service/deployment.yaml
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
