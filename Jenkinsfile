pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'chancho1987'
        IMAGE_NAME     = 'api-service'
        IMAGE_TAG      = "0.1.${env.BUILD_NUMBER}"
        FULL_IMAGE     = "${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
        K8S_NAMESPACE  = 'devops-sre-lab'
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

        stage('Build Docker image (real)') {
            steps {
                sh """
                echo "[INFO] Construyendo imagen Docker ${FULL_IMAGE}"
                docker build -t ${FULL_IMAGE} apps/api-service
                """
            }
        }

        stage('Push image to registry (real)') {
            steps {
                // Aquí asumo que ya tenías otro withCredentials para Docker Hub
                sh """
                echo "[INFO] Pusheando imagen ${FULL_IMAGE}"
                docker push ${FULL_IMAGE}
                """
            }
        }

        stage('Deploy to Kubernetes (GitOps style)') {
            steps {
                // >>> AQUÍ ESTABA EL PROBLEMA <<<
                withCredentials([
                    usernamePassword(
                        credentialsId: 'EcarrilloGitHub',   // ID de tu credencial
                        usernameVariable: 'GIT_USER',
                        passwordVariable: 'GIT_PASS'
                    )
                ]) {   // <--- ESTE BLOQUE { ... } ES OBLIGATORIO

                    sh """
                    echo "[INFO] Actualizando deployment con imagen ${FULL_IMAGE}"

                    # Asegurarnos de estar sobre main
                    git fetch origin
                    git checkout -B main origin/main

                    # Actualizar la imagen en el deployment base
                    sed -i 's|image: .*/api-service:.*|image: ${FULL_IMAGE}|' k8s/base/api-service/deployment.yaml

                    echo "[INFO] Diff de cambios:"
                    git diff k8s/base/api-service/deployment.yaml || true

                    # Config de usuario solo para el commit
                    git config user.email "jenkins@example.com"
                    git config user.name  "Jenkins CI"

                    # Commit si hay cambios
                    git add k8s/base/api-service/deployment.yaml
                    git commit -m "chore: bump api-service image to ${IMAGE_TAG}" || echo "[INFO] No hay cambios para commitear"

                    # Push usando las credenciales de Jenkins
                    git push https://${GIT_USER}:${GIT_PASS}@github.com/Ecarrillo1987/devops-sre-lab.git main
                    """
                }
            }
        }
    }

    post {
        always {
            echo "[INFO] Pipeline finished with status: ${currentBuild.currentResult}"
        }
    }
}
