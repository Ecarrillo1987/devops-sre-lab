pipeline {
    agent any

    environment {
        DOCKER_USER   = "chancho1987"

        IMAGE_NAME    = "api-service"
        IMAGE_REPO    = "${DOCKER_USER}/${IMAGE_NAME}"
        IMAGE_TAG     = "0.1.${env.BUILD_NUMBER}"
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
                docker build -t ${IMAGE_REPO}:${IMAGE_TAG} apps/api-service
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

                    echo "[INFO] Haciendo push de ${IMAGE_REPO}:${IMAGE_TAG}"
                    docker push ${IMAGE_REPO}:${IMAGE_TAG}
                    """
                }
            }
        }

        // 🔹 Actualizar manifiesto de k8s (GitOps style)
        stage('Deploy to Kubernetes (GitOps style)') {
            steps {
                sh """
                echo "[INFO] Actualizando manifiesto de k8s con la nueva imagen..."

                # Opción sencilla: reemplazar la línea de image en el deployment base
                sed -i 's#image: .*api-service:.*#image: ${IMAGE_REPO}:${IMAGE_TAG}#' k8s/base/api-service/deployment.yaml

                echo "[INFO] Diff del archivo actualizado:"
                grep 'image:' -n k8s/base/api-service/deployment.yaml || true

                echo "[INFO] Aquí normalmente haríamos git commit + git push para que ArgoCD lo detecte."
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
