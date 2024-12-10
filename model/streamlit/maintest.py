import streamlit as st
from transformers import pipeline


@st.cache_resource
def load_sentiment_model():
    return pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

sentiment_model = load_sentiment_model()

st.title("Analyse de Sentiment")

user_input = st.text_area("Entrez votre commentaire ici :", placeholder="Tapez un commentaire...")

if st.button("Classer le commentaire"):
    if user_input.strip():

        result = sentiment_model(user_input)
        st.subheader("Résultat de l'analyse :")
        st.write(f"**Sentiment : {result[0]['label']}**")
        st.write(f"**Score : {result[0]['score']:.2f}**")
    else:
        st.warning("Veuillez entrer un commentaire avant de classer.")