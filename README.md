# Application d'Analyse de Sentiment de Tweets

Cette application permet d'analyser le sentiment (positif ou négatif) d'un texte en utilisant un modèle de machine learning pré-entraîné.

## Architecture

L'application est composée de deux parties:

- **Backend**: API FastAPI qui expose le modèle d'analyse de sentiment
- **Frontend**: Interface utilisateur Streamlit simple et intuitive

## Prérequis

- Python 3.9+
- Pip (gestionnaire de paquets Python)

## Installation

1. Clonez ce dépôt:

```bash
git clone <url-du-repo>
cd <nom-du-repo>
```

2. Installez les dépendances:

```bash
pip install -r requirements.txt
```

## Lancement de l'application

1. Démarrez le backend (API FastAPI):

```bash
uvicorn backend:app
```

2. Dans un nouveau terminal, démarrez le frontend (Streamlit):

```bash
streamlit run frontend.py
```

3. Ouvrez votre navigateur à l'adresse indiquée par Streamlit (généralement http://localhost:8501)

## Utilisation

1. Entrez un texte dans la zone de saisie
2. Cliquez sur le bouton "Analyser"
3. Le résultat s'affichera avec:
   - Le sentiment détecté (positif ou négatif)
   - Le pourcentage de confiance du modèle

## Structure des fichiers

- `backend.py`: API FastAPI qui expose le modèle
- `frontend.py`: Interface utilisateur Streamlit
- `best_sentiment_model/`: Dossier contenant le modèle MLflow
- `tokenizer.pkl/`: Dossier contenant le tokenizer
- `requirements.txt`: Liste des dépendances Python

## Documentation de l'API

Une fois le backend démarré, vous pouvez consulter la documentation interactive de l'API à l'adresse:

- http://localhost:8000/docs
