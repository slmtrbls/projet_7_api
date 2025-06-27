#!/usr/bin/env bash

# Script de démarrage pour l'API FastAPI uniquement
# Azure App Service définira la variable PORT automatiquement (par défaut 8000 en local)

set -euo pipefail

PORT="${PORT:-8000}"

exec gunicorn backend:app \
  --workers 2 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:"${PORT}" \
  --timeout 600 