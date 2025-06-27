import pytest
from fastapi.testclient import TestClient
import numpy as np
from unittest.mock import patch, MagicMock

from backend import app

# Client de test
client = TestClient(app)

# Tests de base pour l'API
def test_root_endpoint():
    """Test de l'endpoint racine."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

# Test avec mock pour la prédiction
@patch("backend.model")
@patch("backend.tokenizer")
def test_predict_endpoint(mock_tokenizer, mock_model):
    """Test de l'endpoint de prédiction avec mocks."""
    # Configuration des mocks
    mock_tokenizer.texts_to_sequences.return_value = [[1, 2, 3]]
    mock_tokenizer.texts_to_matrix.return_value = np.array([[0.1, 0.2, 0.3, 0.4]])
    
    # Simuler une prédiction positive avec une confiance de 75%
    mock_model.predict.return_value = np.array([[0.25, 0.75]])
    
    # Appel à l'API
    response = client.post("/predict", json={"text": "Ce texte est positif"})
    
    # Vérifications
    assert response.status_code == 200
    result = response.json()
    assert "sentiment" in result
    assert "confidence" in result
    assert result["sentiment"] == "positif"
    assert isinstance(result["confidence"], float)
    assert 0 <= result["confidence"] <= 100

# Test avec mock pour la prédiction négative
@patch("backend.model")
@patch("backend.tokenizer")
def test_predict_negative(mock_tokenizer, mock_model):
    """Test de l'endpoint de prédiction pour un sentiment négatif."""
    # Configuration des mocks
    mock_tokenizer.texts_to_sequences.return_value = [[1, 2, 3]]
    mock_tokenizer.texts_to_matrix.return_value = np.array([[0.1, 0.2, 0.3, 0.4]])
    
    # Simuler une prédiction négative avec une confiance de 80%
    mock_model.predict.return_value = np.array([[0.8, 0.2]])
    
    # Appel à l'API
    response = client.post("/predict", json={"text": "Ce texte est négatif"})
    
    # Vérifications
    assert response.status_code == 200
    result = response.json()
    assert result["sentiment"] == "négatif"
    assert isinstance(result["confidence"], float)
    assert 0 <= result["confidence"] <= 100

# Test d'erreur - texte vide
def test_predict_empty_text():
    """Test de l'endpoint de prédiction avec un texte vide."""
    response = client.post("/predict", json={"text": ""})
    assert response.status_code == 422  # Validation error

# Test d'erreur - format incorrect
def test_predict_invalid_format():
    """Test de l'endpoint de prédiction avec un format invalide."""
    response = client.post("/predict", json={"invalid_key": "some text"})
    assert response.status_code == 422  # Validation error 