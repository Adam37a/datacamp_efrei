import pandas as pd
import re
from textblob import TextBlob
import os

# Mapping of country codes to English country names
country_mapping = {
    'GB': 'United Kingdom',
    'DE': 'Germany',
    'US': 'United States',
    'RS': 'Serbia',
    'JO': 'Jordan',
    'GR': 'Greece',
    'FR': 'France',
    'QA': 'Qatar',
    'EG': 'Egypt',
    'AU': 'Australia',
    'ZA': 'South Africa',
    'SA': 'Saudi Arabia',
    'ES': 'Spain',
    'DK': 'Denmark',
    'MT': 'Malta',
    'NG': 'Nigeria',
    'CA': 'Canada',
    'CY': 'Cyprus',
    'BE': 'Belgium',
    'JM': 'Jamaica',
    'IT': 'Italy',
    'PT': 'Portugal',
    'NL': 'Netherlands',
    'TZ': 'Tanzania',
    'GI': 'Gibraltar',
    'JE': 'Jersey',
    'VN': 'Vietnam',
    'MX': 'Mexico',
    'AE': 'United Arab Emirates',
    'MC': 'Monaco',
    'NZ': 'New Zealand',
    'MY': 'Malaysia',
    'MU': 'Mauritius',
    'IN': 'India',
    'PK': 'Pakistan',
    'KE': 'Kenya',
    'GG': 'Guernsey',
    'IE': 'Ireland',
    'AT': 'Austria',
    'HR': 'Croatia',
    'NI': 'Nicaragua',
    'SG': 'Singapore',
    'UA': 'Ukraine',
    'HK': 'Hong Kong',
    'IM': 'Isle of Man',
    'DZ': 'Algeria',
    'AG': 'Antigua and Barbuda',
    'KW': 'Kuwait',
    'TT': 'Trinidad and Tobago',
    'ID': 'Indonesia',
    'NO': 'Norway',
    'CH': 'Switzerland'
}

script_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(script_dir, ".."))

file_path = os.path.join(project_root, "scraping", "scrapped_file.csv")

df = pd.read_csv(
    file_path,
    sep=';',
    on_bad_lines='skip',
    encoding='utf-8',
    engine='python'
)

print(df)

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

# Supprimer tous les guillemets doubles (") dans la colonne "Contenu de l'avis"
df['Contenu de l\'avis'] = df['Contenu de l\'avis'].apply(lambda x: x.replace('"', '') if isinstance(x, str) else x)


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



# Supprimer les guillemets de la colonne "Contenu de l'avis"
df['Contenu de l\'avis'] = df['Contenu de l\'avis'].str.replace('"', '', regex=False)

# Remplacement des points-virgules dans la colonne 'contenu_de_l_avis'
df["Contenu de l\'avis"] = df["Contenu de l\'avis"].str.replace(";", "", regex=False)



import csv

project_root = os.path.abspath(os.path.join(script_dir, "..",))
output_folder = os.path.join(project_root, "data_cleaning")
os.makedirs(output_folder, exist_ok=True)
duplicated_file_path = os.path.join(output_folder, "avis_transformes_4.csv")

df.to_csv(
    duplicated_file_path,
    index=False,
    encoding='utf-8',
    sep=";",  # Utiliser ; comme séparateur
    quoting=csv.QUOTE_NONE,  # Désactiver les guillemets automatiques
    escapechar="\\",
    lineterminator='\n'  # Assurer une bonne gestion des retours à la ligne
)
