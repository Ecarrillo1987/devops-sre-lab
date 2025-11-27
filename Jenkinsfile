pipeline {
    agent any

    environment {
        DOCKER_USER   = "chancho1987"
        IMAGE_NAME    = "api-service"
        APP_VERSION   = "0.1"                      
        IMAGE_TAG     = "${APP_VERSION}.${BUILD_NUMBER}"
        FULL_IMAGE    = "${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
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
                echo "[INFO] Aquí normalmente correría tests y lint de la app FastAPI"
                echo "[INFO] Por ejemplo: pytest, mypy, flake8, etc."
                '''
            }
        }

        // 🔹 Build REAL de la imagen Docker
        stage('Build Docker image') {
            steps {
                sh """
                echo "[INFO] Construyendo imagen Docker real..."
                docker build -t ${FULL_IMAGE} apps/api-service
                echo "[INFO] Imagen construida:"
                docker images | grep ${IMAGE_NAME} || true
                """
            }
        }

        // 🔹 Push REAL a Docker Hub
        stage('Push image to registry') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'REG_USER',
                    passwordVariable: 'REG_PASS'
                )]) {
                    sh """
                    echo "[INFO] Login en Docker Hub..."
                    echo "${REG_PASS}" | docker login -u "${REG_USER}" --password-stdin

                    echo "[INFO] Pushing image ${FULL_IMAGE}"
                    docker push ${FULL_IMAGE}
                    """
                }
            }
        }

        // 🔹 Actualizar manifiesto de k8s (GitOps style)
        stage('Deploy to Kubernetes (GitOps style)') {
            steps {
                sh """
                echo "[INFO] Actualizando deployment con imagen ${FULL_IMAGE}"

                # Opción sencilla: reemplazar la línea de image en el deployment base
                sed -i 's|image: .*/api-service:.*|image: ${FULL_IMAGE}|' k8s/base/api-service/deployment.yaml

                git config user.email "jenkins@example.com"
                git config user.name  "Jenkins CI"
                git status

                git commit -am "chore: bump api-service image to ${IMAGE_TAG}" || echo "No hay cambios que commitear"
                git push origin main
                """
            }
        }
    }

    post {
        always {
            echo "[INFO] Pipeline finished with status: ${currentBuild.currentResult}"
        }
    }
}
