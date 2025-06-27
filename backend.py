import os
# Essayer d'utiliser pickle5 si disponible, sinon utiliser pickle standard
try:
    import pickle5 as pickle
except ImportError:
    import pickle
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
import tensorflow as tf
from tensorflow import keras

# Définition du modèle de données pour l'API
class TweetRequest(BaseModel):
    text: str
    
    @validator('text')
    def text_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Le texte ne peut pas être vide")
        return v

class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float

# Initialisation de l'API
app = FastAPI(title="API d'Analyse de Sentiment")

# Initialisation des variables globales
model = None
tokenizer = None

# Chargement du modèle et du tokenizer
@app.on_event("startup")
async def load_model():
    global model, tokenizer
    
    try:
        # Chargement direct du modèle Keras (on contourne MLflow)
        model_path = os.path.join(os.path.dirname(__file__), "best_sentiment_model", "data", "model.keras")
        model = keras.models.load_model(model_path)
        
        # Chargement du tokenizer
        tokenizer_path = os.path.join(os.path.dirname(__file__), "tokenizer.pkl", "tmpaqfbp_4q.pkl")
        with open(tokenizer_path, "rb") as f:
            tokenizer = pickle.load(f)
            
        print("Modèle et tokenizer chargés avec succès!")
    except Exception as e:
        print(f"Erreur lors du chargement du modèle ou du tokenizer: {e}")
        raise e

# Prétraitement du texte et prédiction
def preprocess_and_predict(text):
    # Vérifier que le tokenizer et le modèle sont chargés
    if tokenizer is None or model is None:
        raise ValueError("Le modèle ou le tokenizer n'est pas chargé")
        
    # Tokenization du texte
    sequence = tokenizer.texts_to_sequences([text])
    
    # Padding pour avoir une longueur fixe (12 d'après la signature du modèle)
    max_length = 12
    if len(sequence[0]) > max_length:
        sequence[0] = sequence[0][:max_length]
    else:
        sequence[0] = sequence[0] + [0] * (max_length - len(sequence[0]))
    
    # Conversion en array numpy
    sequence_array = np.array(sequence)
    
    # Prédiction
    prediction = model.predict(sequence_array)
    
    # Interprétation de la prédiction
    sentiment_index = np.argmax(prediction[0])
    confidence = float(prediction[0][sentiment_index])
    
    sentiment = "positif" if sentiment_index == 1 else "négatif"
    
    return sentiment, confidence

# Endpoint pour l'analyse de sentiment
@app.post("/predict", response_model=SentimentResponse)
async def predict_sentiment(request: TweetRequest):
    try:
        sentiment, confidence = preprocess_and_predict(request.text)
        return {"sentiment": sentiment, "confidence": confidence * 100}  # Pourcentage de confiance
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction: {str(e)}")

# Route de test pour vérifier que l'API fonctionne
@app.get("/")
async def root():
    return {"message": "API d'analyse de sentiment opérationnelle"}

# Pour lancer l'API: uvicorn backend:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 