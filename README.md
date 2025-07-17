# MELANO INC – Documentación Técnica de Arquitectura con Agentes IA Interconectados

## 🏗️ ARQUITECTURA DE AGENTES

```text
[Usuario] ─ Dashboard Web / App Mobile
        │
        ▼
[Agent Hermes] ─ Leads y Ventas
        │
        ├──► [Agent Ares] ─ Bots de Inversión (Scalping / Arbitraje / Tendencias)
        │
        ├──► [Agent Chronos] ─ Automatización de Flujo (Onboarding, Activaciones)
        │
        └──► [Agent Athena] ─ Analítica y Rendimiento
        │
        ▼
[Melania OS] ─ Orquestadora Central (Lógica, IA, Seguridad, APIs)
        │
        ▼
[Infraestructura Cloud + Base de Datos + Logging Centralizado]
```

## 📦 DEPLOYMENT PIPELINE

- CI/CD: GitHub Actions + Docker Build
- Auto-deploy si tests y linters pasan
- Notificaciones en Slack vía Agent Chronos


## 🚀 Quickstart

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn melania.main:app --reload

# Run tests
pytest
```
