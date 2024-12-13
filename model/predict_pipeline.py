import pandas as pd
from transformers import pipeline
import os
import shutil

positive_keywords = ["excellent", "superb", "amazing", "fast", "great"]
negative_keywords = ["bad", "terrible", "horrible", "slow", "poor"]

def preprocess_text(text):
    if not isinstance(text, str):
        return "Avis non fourni"

    for word in positive_keywords:
        text = text.replace(word, f"**{word.upper()}**")
    for word in negative_keywords:
        text = text.replace(word, f"__{word.upper()}__")

    context = "This is a customer review: "
    return context + text

if __name__ == '__main__':
    input_file_path = "avis_transformes_4.csv"
    output_folder = r"datacamp_efrei/model/streamlit"
    os.makedirs(output_folder, exist_ok=True)
    duplicated_file_path = os.path.join(output_folder, "luggage_predicted_review_pipeline_model.csv")

    try:
        shutil.copy(input_file_path, duplicated_file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Fichier introuvable : {input_file_path}")

    df = pd.read_csv(duplicated_file_path, encoding='utf-8', delimiter=';')
    if "Contenu de l'avis" not in df.columns:
        raise KeyError("La colonne 'Contenu de l'avis' est absente du fichier CSV.")

    df["Contenu de l'avis"] = df["Contenu de l'avis"].fillna("Avis non fourni")
    df["Contenu de l'avis"] = df["Contenu de l'avis"].apply(preprocess_text)
    pipe = pipeline("text-classification", model="nlptown/bert-base-multilingual-uncased-sentiment")

    def predict_sentiment(text):
        try:
            result = pipe(text, truncation=True)[0]
            return int(result['label'].split()[0])
        except Exception as e:
            print(f"Erreur pour le texte suivant : {text}. Erreur : {e}")
            return None

    df['Predicted Sentiment'] = df["Contenu de l'avis"].apply(predict_sentiment)
    df.to_csv(duplicated_file_path, index=False, encoding='utf-8-sig')
    print(f"Fichier traité enregistré dans : {duplicated_file_path}")
