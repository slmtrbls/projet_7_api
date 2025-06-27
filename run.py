# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import time


def main():
    print("=== Application Sentiment Analysis ===")

    # Vérifier la version de Python (utile pour le diagnostic)
    print("Python version:")
    print(sys.version)

    # --------- Gestion des ports ---------
    # Port exposé publiquement par Azure App Service
    public_port = int(os.environ.get("PORT", "8000"))

    # Port interne pour le backend (non exposé)
    backend_port = public_port + 1  # ex: 8001

    # Fixer l'URL du backend pour que le frontend Streamlit puisse l'appeler
    os.environ["API_URL"] = f"http://localhost:{backend_port}"

    print(f"Public port  : {public_port}")
    print(f"Backend port : {backend_port}")
    print(f"API_URL      : {os.environ['API_URL']}")

    # --------- Lancement du backend FastAPI ---------
    print("Starting backend (FastAPI)...")
    backend_cmd = (
        f"gunicorn backend:app "
        f"--bind=0.0.0.0:{backend_port} "
        f"--workers=2 --timeout 600"
    )
    backend_process = subprocess.Popen(backend_cmd, shell=True)

    # Laisser le temps au backend de démarrer
    time.sleep(3)

    # --------- Lancement du frontend Streamlit ---------
    print("Starting frontend (Streamlit)...")
    frontend_cmd = (
        f"streamlit run frontend.py "
        f"--server.port={public_port} "
        f"--server.address=0.0.0.0"
    )
    frontend_process = subprocess.Popen(frontend_cmd, shell=True)

    # --------- Attente des processus ---------
    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("Stopping application...")
        backend_process.terminate()
        frontend_process.terminate()


if __name__ == "__main__":
    main() 