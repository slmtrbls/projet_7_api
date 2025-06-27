import pytest
from unittest.mock import patch, MagicMock
import requests
import json
import streamlit as st
import sys
import os
import importlib.util

# Import du module frontend.py
def import_frontend():
    """Importe le module frontend.py pour les tests."""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend.py")
    spec = importlib.util.spec_from_file_location("frontend", frontend_path)
    frontend = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(frontend)
    return frontend

# Patch pour Streamlit
@pytest.fixture
def mock_streamlit():
    """Mock pour les fonctions Streamlit."""
    with patch("streamlit.title") as mock_title, \
         patch("streamlit.markdown") as mock_markdown, \
         patch("streamlit.text_area") as mock_text_area, \
         patch("streamlit.button") as mock_button, \
         patch("streamlit.spinner") as mock_spinner, \
         patch("streamlit.success") as mock_success, \
         patch("streamlit.error") as mock_error, \
         patch("streamlit.progress") as mock_progress, \
         patch("streamlit.set_page_config") as mock_set_page_config, \
         patch("streamlit.warning") as mock_warning:
        
        mock_text_area.return_value = "Exemple de texte"
        mock_button.return_value = True
        
        yield {
            "title": mock_title,
            "markdown": mock_markdown,
            "text_area": mock_text_area,
            "button": mock_button,
            "spinner": mock_spinner,
            "success": mock_success,
            "error": mock_error,
            "progress": mock_progress,
            "set_page_config": mock_set_page_config,
            "warning": mock_warning
        }

# Test de la fonction get_prediction
@patch("requests.post")
def test_get_prediction_success(mock_post):
    """Test de la fonction get_prediction avec succès."""
    # Configuration du mock
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "sentiment": "positif",
        "confidence": 75.5
    }
    mock_post.return_value = mock_response
    
    # Import du module frontend
    frontend = import_frontend()
    
    # Appel de la fonction
    result = frontend.get_prediction("Exemple de texte positif")
    
    # Vérifications
    assert result is not None
    assert result["sentiment"] == "positif"
    assert result["confidence"] == 75.5
    mock_post.assert_called_once()

# Test de la fonction get_prediction avec erreur
@patch("requests.post")
def test_get_prediction_error(mock_post):
    """Test de la fonction get_prediction avec erreur."""
    # Configuration du mock pour simuler une erreur
    mock_post.side_effect = requests.exceptions.RequestException("Erreur de connexion")
    
    # Import du module frontend
    frontend = import_frontend()
    
    # Appel de la fonction
    result = frontend.get_prediction("Exemple de texte")
    
    # Vérifications
    assert result is None
    mock_post.assert_called_once()

# Test du comportement de l'interface
@patch("frontend.get_prediction")
def test_ui_behavior(mock_get_prediction, mock_streamlit):
    """Test du comportement de l'interface utilisateur."""
    # Configuration du mock
    mock_get_prediction.return_value = {
        "sentiment": "positif",
        "confidence": 75.5
    }
    
    # Import et exécution du module frontend
    with patch.dict(sys.modules, {"streamlit": st}):
        frontend = import_frontend()
        # Appel explicite de la fonction main
        frontend.main()
    
    # Vérifications
    mock_streamlit["title"].assert_called_once()
    mock_streamlit["text_area"].assert_called_once()
    mock_streamlit["button"].assert_called_once() 