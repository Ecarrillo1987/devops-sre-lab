# DevOps SRE Lab – FastAPI + Jenkins + ArgoCD + Kubernetes

Laboratorio práctico de DevOps / SRE donde se implementa un flujo **CI/CD + GitOps** completo para una API en FastAPI desplegada en Kubernetes, con **entornos `dev` y `prod`** separados.

## Objetivos

- Construir y versionar una imagen Docker de una API (FastAPI).
- Publicar la imagen en Docker Hub (`chancho1987/api-service`).
- Actualizar manifiestos de Kubernetes de forma automatizada desde Jenkins (**GitOps**).
- Gestionar despliegues en K8s con **ArgoCD**, usando `kustomize` y overlays por entorno.
- Aplicar buenas prácticas SRE: namespaces, requests/limits, HPA, secrets, multi–ambiente.

---

## Arquitectura

### Diagrama general (CI/CD + GitOps)

```mermaid
flowchart LR
    Dev[Developer\nVS Code] -->|git push| GitHub

    subgraph CI[Jenkins CI]
        J1[Checkout código] --> J2[Tests / Lint (simulado)]
        J2 --> J3[Build imagen Docker\nchancho1987/api-service:TAG]
        J3 --> J4[Push a Docker Hub]
        J4 --> J5[Actualizar manifiesto K8s\n(k8s/base/api-service/deployment.yaml)]
        J5 --> J6[Commit & Push a GitHub]
    end

    GitHub -->|webhook/poll SCM| CI
    GitHub -->|GitOps| ArgoCD

    subgraph GitOps[ArgoCD]
        A1[App api-service-dev\npath: k8s/overlays/dev/api-service] --> K8sDev
        A2[App api-service-prod\npath: k8s/overlays/prod/api-service] --> K8sProd
    end

    subgraph Cluster[Kubernetes Cluster]
        K8sDev[Namespace devops-sre-lab\nDeployment+Service+Secret+HPA]
        K8sProd[Namespace devops-sre-lab-prod\nDeployment+Service+Secret+HPA]
    end

    UserDev[Usuario Dev] -->|HTTP| ApiDev[api-dev.local:30082/docs]
    UserProd[Usuario Prod] -->|HTTP| ApiProd[api-prod.local:30083/docs]

Stack tecnológico

Aplicación: FastAPI (Python) – apps/api-service

Contenedores: Docker

Registry: Docker Hub → usuario chancho1987

CI: Jenkins (en contenedor Docker)

Git: GitHub (Ecarrillo1987/devops-sre-lab)

GitOps / CD: ArgoCD

Orquestador: Kubernetes (Docker Desktop / kind)

Plantillas K8s: Kustomize (base + overlays dev/prod)

.
├── apps/
│   └── api-service/                 # Código de la API FastAPI
│
├── argo/
│   ├── api-service-dev-app.yaml     # Definición de App ArgoCD (dev)
│   └── api-service-prod-app.yaml    # Definición de App ArgoCD (prod)
│
├── cicd/                            # (Opcional) scripts auxiliares de CI
│
├── k8s/
│   ├── base/
│   │   ├── api-service/
│   │   │   ├── deployment.yaml      # Deployment base (imagen, probes, etc.)
│   │   │   ├── service.yaml         # Service base
│   │   │   ├── hpa.yaml             # HPA base
│   │   │   └── kustomization.yaml
│   │   └── namespace.yaml           # Namespace base dev (devops-sre-lab)
│   │
│   └── overlays/
│       ├── dev/
│       │   └── api-service/
│       │       ├── kustomization.yaml
│       │       └── secret-sre.yaml  # Secret con TEAM=SRE para dev
│       │
│       └── prod/
│           └── api-service/
│               ├── kustomization.yaml
│               ├── namespace.yaml   # Namespace prod (devops-sre-lab-prod)
│               ├── resources-prod.yaml # Parches de replicas/CPU/Mem para prod
│               └── service-prod.yaml   # Parchado de NodePort para prod
│
├── vault/
│   └── k8s/                         # (Reservado para pruebas con Vault)
│
├── Jenkinsfile                      # Pipeline declarativo de Jenkins
└── README.md
