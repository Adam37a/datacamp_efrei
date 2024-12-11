import pandas as pd
import re
import emoji
from textblob import TextBlob


# Mapping des codes pays
country_mapping = {
    'GB': 'Royaume-Uni',
    'DE': 'Allemagne',
    'US': 'États-Unis',
    'RS': 'Serbie',
    'JO': 'Jordanie',
    'GR': 'Grèce',
    'FR': 'France',
    'QA': 'Qatar',
    'EG': 'Égypte',
    'AU': 'Australie',
    'ZA': 'Afrique du Sud',
    'SA': 'Arabie Saoudite',
    'ES': 'Espagne',
    'DK': 'Danemark',
    'MT': 'Malte',
    'NG': 'Nigeria',
    'CA': 'Canada',
    'CY': 'Chypre',
    'BE': 'Belgique',
    'JM': 'Jamaïque',
    'IT': 'Italie',
    'PT': 'Portugal',
    'NL': 'Pays-Bas',
    'TZ': 'Tanzanie',
    'GI': 'Gibraltar',
    'JE': 'Jersey',
    'VN': 'Vietnam',
    'MX': 'Mexique',
    'AE': 'Émirats arabes unis',
    'MC': 'Monaco',
    'NZ': 'Nouvelle-Zélande',
    'MY': 'Malaisie',
    'MU': 'Maurice',
    'IN': 'Inde',
    'PK': 'Pakistan',
    'KE': 'Kenya',
    'GG': 'Guernesey',
    'IE': 'Irlande',
    'AT': 'Autriche',
    'HR': 'Croatie',
    'NI': 'Nicaragua',
    'SG': 'Singapour',
    'UA': 'Ukraine',
    'HK': 'Hong Kong',
    'IM': 'Île de Man',
    'DZ': 'Algérie',
    'AG': 'Antigua-et-Barbuda',
    'KW': 'Koweït',
    'TT': 'Trinité-et-Tobago',
    'ID': 'Indonésie',
    'NO': 'Norvège',
    'CH': 'Suisse'
}

# Lire le fichier CSV (avec séparateur ;)
df = pd.read_csv(
    r"C:\Users\fayca\Documents\GitHub\datacamp_efrei\luggage_superstore_reviews (1).csv",
    sep=';',  # Changez le séparateur si nécessaire
    on_bad_lines='skip',  # Ignore les lignes mal formatées
    encoding='utf-8',  # Spécifiez l'encodage si besoin
    engine='python'  # Utilisez le moteur Python pour une meilleure gestion des erreurs
)

# Remplacer les codes des pays par les noms complets
df['Pays'] = df['Pays'].map(country_mapping)

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

import re

# Fonction pour supprimer les guillemets doubles
def remove_non_linguistic(text):
    return re.sub(r'"', '', text)

# Appliquer la fonction sur la colonne "Contenu de l'avis"
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
df.to_csv('avis_transformes_4.csv', index=False, encoding='utf-8')
