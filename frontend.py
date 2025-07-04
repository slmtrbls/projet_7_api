import streamlit as st
import requests
import json
import os

# URL de l'API backend
API_URL = os.environ.get("API_URL", "http://localhost:8000")
PREDICT_ENDPOINT = f"{API_URL}/predict"

# Fonction pour appeler l'API
def get_prediction(text):
    try:
        response = requests.post(
            PREDICT_ENDPOINT,
            headers={"Content-Type": "application/json"},
            data=json.dumps({"text": text})
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur {response.status_code}: {response.text}")
            return None
    except Exception as e:
        st.error(f"Erreur de connexion à l'API: {str(e)}")
        return None

def main():
    # Configuration de la page
    st.set_page_config(
        page_title="Analyse de Sentiment de Tweets",
        page_icon="🐦",
        layout="centered"
    )

    # Titre et description
    st.title("Analyse de Sentiment de Tweets 🐦")
    st.markdown("""
    Cette application analyse le sentiment d'un texte et détermine s'il est positif ou négatif.
    Entrez votre texte ci-dessous et cliquez sur 'Analyser'.
    """)

    # Zone de saisie du texte
    user_input = st.text_area("Entrez votre texte ici:", height=150)

    # Bouton d'analyse
    if st.button("Analyser"):
        if user_input:
            with st.spinner("Analyse en cours..."):
                result = get_prediction(user_input)
                
                if result:
                    # Affichage du résultat
                    sentiment = result["sentiment"]
                    confidence = result["confidence"]
                    
                    # Stocker pour usage ultérieur
                    st.session_state["last_result"] = {
                        "text": user_input,
                        "sentiment": sentiment,
                        "confidence": confidence,
                    }
                    
                    # Choix de la couleur en fonction du sentiment
                    color = "green" if sentiment == "positif" else "red"
                    
                    # Affichage du résultat avec une mise en forme
                    st.markdown(f"""
                    ## Résultat de l'analyse
                    
                    - **Sentiment détecté:** <span style='color:{color};font-weight:bold'>{sentiment.upper()}</span>
                    - **Niveau de confiance:** {confidence:.2f}%
                    """, unsafe_allow_html=True)
                                    
        else:
            st.warning("Veuillez entrer un texte à analyser.")

    # Si un résultat précédent existe et qu'on n'est pas en train d'analyser, proposer le feedback
    if "last_result" in st.session_state and not st.session_state.get("_streamlit_analyze_clicked", False):
        last = st.session_state["last_result"]
        feedback_comment = st.text_input("Commentaire (facultatif)")
        if st.button("Signaler une erreur de prédiction"):
            payload = {
                "text": last["text"],
                "predicted": last["sentiment"],
                "comment": feedback_comment or None,
            }
            try:
                r = requests.post(f"{API_URL}/feedback", json=payload, timeout=10)
                st.success("Feedback envoyé ! Merci.")
            except Exception as e:
                st.error(f"Erreur d'envoi du feedback : {e}")

# Pour lancer l'application: streamlit run frontend.py
if __name__ == "__main__":
    main() 