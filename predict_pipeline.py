import pandas as pd
from transformers import pipeline
import os
import shutil

# Liste de mots-clés
positive_keywords = ["excellent", "superb", "amazing", "fast", "great"]
negative_keywords = ["bad", "terrible", "horrible", "slow", "poor"]

# Fonction de prétraitement
def preprocess_text(text):
    """
    Prétraite un texte en accentuant les mots-clés et en ajoutant du contexte.
    """
    if not isinstance(text, str):
        return "Avis non fourni"  # Texte par défaut si le texte est invalide

    # Accentuer les mots-clés
    for word in positive_keywords:
        text = text.replace(word, f"**{word.upper()}**")
    for word in negative_keywords:
        text = text.replace(word, f"__{word.upper()}__")

    # Ajouter un contexte
    context = "This is a customer review: "
    return context + text

# Vérifiez que le script est exécuté depuis __main__
if __name__ == '__main__':
    # Chemins des fichiers
    input_file_path = "avis_transformes_4.csv"
    output_folder = "/Users/wassim/Documents/datacamp_efrei/prediction"
    os.makedirs(output_folder, exist_ok=True)
    duplicated_file_path = os.path.join(output_folder, "luggage_predicted_review.csv")

    # Copier le fichier source
    try:
        shutil.copy(input_file_path, duplicated_file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Fichier introuvable : {input_file_path}")

    # Charger les données
    df = pd.read_csv(duplicated_file_path, encoding='utf-8', delimiter=';')
    if "Contenu de l'avis" not in df.columns:
        raise KeyError("La colonne 'Contenu de l'avis' est absente du fichier CSV.")

    # Remplacer les NaN par une chaîne vide
    df["Contenu de l'avis"] = df["Contenu de l'avis"].fillna("Avis non fourni")

    # Prétraiter les textes
    df["Contenu de l'avis"] = df["Contenu de l'avis"].apply(preprocess_text)

    # Initialiser le pipeline
    pipe = pipeline("text-classification", model="nlptown/bert-base-multilingual-uncased-sentiment")

    # Appliquer le modèle sur chaque avis
    def predict_sentiment(text):
        try:
            result = pipe(text, truncation=True)[0]
            return int(result['label'].split()[0])
        except Exception as e:
            print(f"Erreur pour le texte suivant : {text}. Erreur : {e}")
            return None

    df['Predicted Sentiment'] = df["Contenu de l'avis"].apply(predict_sentiment)

    # Sauvegarder les résultats
    df.to_csv(duplicated_file_path, index=False, encoding='utf-8-sig')
    print(f"Fichier traité enregistré dans : {duplicated_file_path}")
