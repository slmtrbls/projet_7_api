# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import time
import shutil


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


# ------------------------------------------------------------
# Helper: ensure pip is available and install dependencies
# ------------------------------------------------------------


def install_dependencies():
    """Install required packages listed in requirements.txt.

    1. S'assure que 'pip' est disponible.
    2. Installe les dépendances si 'gunicorn' ou 'streamlit' manquent.
    """

    def pip_available():
        return shutil.which("pip") is not None

    # Vérifier si gunicorn est déjà disponible
    if shutil.which("gunicorn") and shutil.which("streamlit"):
        print("Dependencies already present – skipping installation")
        return

    print("Installing Python dependencies ...")

    # Étape 1 : s'assurer que pip existe
    if not pip_available():
        print("pip not found – bootstrapping with ensurepip ...")
        try:
            import ensurepip  # lazy import
            ensurepip.bootstrap(upgrade=True)
        except Exception as e:
            print(f"ensurepip failed: {e}. Falling back to get-pip.py …")
            # Télécharger get-pip.py
            try:
                subprocess.check_call([
                    "curl",
                    "https://bootstrap.pypa.io/get-pip.py",
                    "-o",
                    "get-pip.py",
                ])
                subprocess.check_call([sys.executable, "get-pip.py", "--user"])
            except Exception as ee:
                print(f"get-pip failed as well: {ee}")
                print("Unable to install pip – exiting …")
                sys.exit(1)

    # Étape 2 : installer les requirements
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--no-cache-dir", "-r", "requirements.txt"]
        )
    except subprocess.CalledProcessError as inst_err:
        print(f"pip install failed: {inst_err}")
        sys.exit(1)


install_dependencies()


if __name__ == "__main__":
    main() 