# Application d'Analyse de Sentiment de Tweets

Cette application permet d'analyser le sentiment (positif ou négatif) d'un texte en utilisant un modèle de machine learning pré-entraîné.

## Architecture

L'application est composée de deux parties:

- **Backend**: API FastAPI qui expose le modèle d'analyse de sentiment
- **Frontend**: Interface utilisateur Streamlit simple et intuitive

## Prérequis

- Python 3.9+
- Pip (gestionnaire de paquets Python)
- Docker (optionnel, pour le développement avec conteneurs)

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

### Méthode 1: Directement avec Python

1. Démarrez le backend (API FastAPI):

```bash
uvicorn backend:app --reload
```

2. Dans un nouveau terminal, démarrez le frontend (Streamlit):

```bash
streamlit run frontend.py
```

### Méthode 2: Avec Docker Compose

```bash
docker-compose up
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
- `tests/`: Dossier contenant les tests unitaires
- `.github/workflows/`: Configuration CI/CD pour GitHub Actions
- `Dockerfile`: Configuration pour la conteneurisation
- `docker-compose.yml`: Configuration pour le développement local avec Docker
- `azure.yaml`: Configuration pour le déploiement sur Azure

## Tests

Pour exécuter les tests unitaires:

```bash
pytest
```

Pour exécuter les tests avec rapport de couverture:

```bash
pytest --cov=./ --cov-report=html
```

## CI/CD avec GitHub Actions

Ce projet est configuré avec GitHub Actions pour:

1. **Tests automatiques**: Exécution des tests à chaque push et pull request
2. **Déploiement continu**: Déploiement automatique sur Azure Web App après les tests réussis sur la branche main

### Configuration pour le déploiement

Pour configurer le déploiement sur Azure Web App:

1. Créez une Web App sur Azure
2. Récupérez le profil de publication depuis le portail Azure
3. Ajoutez-le comme secret GitHub nommé `AZURE_WEBAPP_PUBLISH_PROFILE`

## Documentation de l'API

Une fois le backend démarré, vous pouvez consulter la documentation interactive de l'API à l'adresse:

- http://localhost:8000/docs
