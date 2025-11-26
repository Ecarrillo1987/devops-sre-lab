from fastapi import FastAPI
from datetime import datetime

app = FastAPI(title="API Service", version="0.1.0")


@app.get("/")
def read_root():
    return {
        "message": "API Service up and running",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "environment": "local",
        "version": "0.1.0",
    }


@app.get("/info")
def info():
    return {
        "service": "api-service",
        "owner": "Erick",
        "description": "Demo API for DevOps/SRE lab with Jenkins + Kubernetes + ArgoCD",
    }
