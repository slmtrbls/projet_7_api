# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import time

def main():
    print("Starting application...")
    
    # Verifier la version de Python
    print("Python version:")
    print(sys.version)
    
    # Installation des dependances
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-cache-dir", "-r", "requirements.txt"])
    
    # Definir le port
    port = os.environ.get('PORT', '8000')
    print("Using port: {}".format(port))
    
    # Demarrer le backend
    print("Starting backend...")
    backend_cmd = "gunicorn backend:app --bind=0.0.0.0:{} --workers=2 --timeout 600".format(port)
    backend_process = subprocess.Popen(backend_cmd, shell=True)
    
    # Attendre un peu pour que le backend démarre
    time.sleep(5)
    
    # Demarrer le frontend
    print("Starting frontend...")
    frontend_cmd = "streamlit run frontend.py --server.port=8501 --server.address=0.0.0.0"
    frontend_process = subprocess.Popen(frontend_cmd, shell=True)
    
    # Attendre que les processus se terminent
    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("Stopping application...")
        backend_process.terminate()
        frontend_process.terminate()

if __name__ == "__main__":
    main() 