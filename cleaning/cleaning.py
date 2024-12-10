import pandas as pd
import re
import emoji
from textblob import TextBlob

# Load your dataset
df = pd.read_csv(r"C:\Users\fayca\Documents\GitHub\datacamp_efrei\scraping\luggage_superstore_reviews.csv")

# Normalize ratings: Extract numerical values from the `Note` column
df['Note'] = df['Note'].str.extract(r'(\d+)').astype(int)

# Remove extra whitespace and clean text
df["Contenu de l'avis"] = df["Contenu de l'avis"].apply(lambda x: re.sub(r'\s+', ' ', str(x)).strip())

# Supprimer les lignes où "Contenu de l'avis" est vide (NaN ou équivalent)
df = df.dropna(subset=["Contenu de l'avis"])

# Supprimer les lignes où "Contenu de l'avis" est NaN ou vide
df = df[df["Contenu de l'avis"].notna()]  # Supprime les NaN
df = df[df["Contenu de l'avis"] != 'nan']  # Supprime les lignes contenant 'nan' comme texte



# Convertir les textes en minuscules
df["Contenu de l'avis"] = df["Contenu de l'avis"].str.lower()

def clean_whitespace(text):
    return re.sub(r'\s+', ' ', text).strip()

df["Contenu de l'avis"] = df["Contenu de l'avis"].apply(clean_whitespace)

# Supprimer les caractères non linguistiques
def remove_non_linguistic(text):
    return re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)

df["Contenu de l'avis"] = df["Contenu de l'avis"].apply(remove_non_linguistic)

# Convert "Date de publication" to datetime format
df["Date de publication"] = pd.to_datetime(df["Date de publication"])

# Fonction pour corriger les fautes d'orthographe
def correct_spelling(text):
    blob = TextBlob(text)
    corrected_text = blob.correct()
    return str(corrected_text)

# Exemple d'utilisation
text = "I loved thiss!!!"
corrected_text = correct_spelling(text)

# Remplacer les emojis par des descriptions textuelles
def replace_emojis(text):
    return emoji.demojize(text, delimiters=("", ""))

# Appliquer la fonction à la colonne "Contenu de l'avis"
df["Contenu de l'avis"] = df["Contenu de l'avis"].apply(replace_emojis)



# Exporter le DataFrame en fichier CSV
df.to_csv('avis_transformes.csv', index=False, encoding='utf-8')
