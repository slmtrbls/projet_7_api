import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import numpy as np
import os
import sys

# Ajouter le répertoire parent au chemin Python pour pouvoir importer les modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend import app

@pytest.fixture
def client():
    """Fixture qui fournit un client de test pour l'API FastAPI."""
    return TestClient(app)

@pytest.fixture
def mock_model():
    """Fixture qui fournit un mock pour le modèle TensorFlow."""
    with patch("backend.model") as mock:
        # Configuration du mock pour simuler une prédiction
        mock.predict.return_value = np.array([[0.3, 0.7]])
        yield mock

@pytest.fixture
def mock_tokenizer():
    """Fixture qui fournit un mock pour le tokenizer."""
    with patch("backend.tokenizer") as mock:
        # Configuration du mock pour simuler la tokenisation
        mock.texts_to_sequences.return_value = [[1, 2, 3]]
        mock.texts_to_matrix.return_value = np.array([[0.1, 0.2, 0.3, 0.4]])
        yield mock

@pytest.fixture
def sample_text():
    """Fixture qui fournit un exemple de texte pour les tests."""
    return "Ceci est un exemple de texte pour les tests."

@pytest.fixture
def sample_prediction_positive():
    """Fixture qui fournit un exemple de prédiction positive."""
    return {
        "sentiment": "positif",
        "confidence": 70.0
    }

@pytest.fixture
def sample_prediction_negative():
    """Fixture qui fournit un exemple de prédiction négative."""
    return {
        "sentiment": "négatif",
        "confidence": 65.0
    } 