# DevOps / SRE Lab

Este repositorio es un laboratorio personal para practicar y demostrar habilidades de:

- CI/CD con Jenkins (pipeline as code)
- Contenedores con Docker
- Despliegues en Kubernetes (deployments, services, ingresses, configmaps, secrets)
- GitOps con ArgoCD (promociones DEV → QA → UAT → PROD)
- Manejo de secretos con Hashicorp Vault (flujo conceptual)
- Integración con herramientas de calidad (SonarQube / análisis estático)

La idea es simular un escenario similar al rol de Especialista DevOps / SRE:

- Automatizar pipelines de build, test y despliegue.
- Gestionar promociones entre ambientes a través de GitOps.
- Monitorear y diagnosticar fallas de despliegue.
- Colaborar con equipos de Backend, QA y Arquitectura.

Este lab se ejecuta en un clúster local de Kubernetes (Docker Desktop) y todas las definiciones de infraestructura y aplicaciones se mantienen como código en este repositorio.
