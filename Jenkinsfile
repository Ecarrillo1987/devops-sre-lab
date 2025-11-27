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
                withCredentials([
                    usernamePassword(
                        credentialsId: 'EcarrilloGitHub',   // <-- ID de la credencial de tu captura
                        usernameVariable: 'GIT_USER',
                        passwordVariable: 'GIT_PASS'
                    )
                ]) 
                sh """
                echo "[INFO] Actualizando deployment con imagen ${FULL_IMAGE}"

                git fetch origin
                git checkout -B main origin/main

                sed -i 's|image: .*/api-service:.*|image: ${FULL_IMAGE}|' k8s/base/api-service/deployment.yaml

                echo "[INFO] Diff de cambios:"
                git diff k8s/base/api-service/deployment.yaml || true

                git config user.email "jenkins@example.com"
                git config user.name  "Jenkins CI"

                git add k8s/base/api-service/deployment.yaml
                git commit -m "chore: bump api-service image to ${IMAGE_TAG}" || echo "[INFO] No hay cambios para commitear"

                git push https://${GIT_USER}:${GIT_PASS}@github.com/Ecarrillo1987/devops-sre-lab.git main

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
