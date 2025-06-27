#!/bin/bash

# Installation des dependances
echo "Installing dependencies..."
pip install --no-cache-dir -r requirements.txt

# Definition du port pour Azure (utilise la variable PORT d'Azure ou 8000 par défaut)
PORT=${PORT:-8000}
STREAMLIT_PORT=8501

echo "Starting application on port $PORT"

# Demarrage du backend FastAPI
gunicorn backend:app --bind=0.0.0.0:$PORT --workers=2 --timeout 600 --access-logfile=- --error-logfile=- &
BACKEND_PID=$!

# Demarrage du frontend Streamlit
streamlit run frontend.py --server.port=$STREAMLIT_PORT --server.address=0.0.0.0 &
FRONTEND_PID=$!

# Attendre que les deux processus se terminent
wait $BACKEND_PID $FRONTEND_PID 