FROM python:3.9-slim

WORKDIR /app

# Installation des outils de compilation nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copie des fichiers de l'application
COPY requirements.txt .
COPY backend.py .
COPY frontend.py .
COPY startup.sh .
COPY best_sentiment_model/ ./best_sentiment_model/
COPY tokenizer.pkl/ ./tokenizer.pkl/

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Rendre le script de démarrage exécutable
RUN chmod +x startup.sh

# Exposer les ports pour FastAPI et Streamlit
EXPOSE 8000
EXPOSE 8501

# Commande de démarrage
CMD ["./startup.sh"] 