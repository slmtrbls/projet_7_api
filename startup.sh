#!/bin/bash

# Installation des dépendances
pip install -r requirements.txt

# Démarrage du backend FastAPI
gunicorn backend:app --bind=0.0.0.0:8000 --workers=4 --daemon

# Démarrage du frontend Streamlit
streamlit run frontend.py --server.port=8501 --server.address=0.0.0.0 