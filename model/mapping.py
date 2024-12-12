import pandas as pd
import csv

df = pd.read_csv(r"C:\Users\fayca\Documents\GitHub\datacamp_efrei\prediction\luggage_superstore_reviews.csv")

# Dictionnaire pour mapper les notes à des descriptions
mapping = {
    1: "Négatif fort",
    2: "Négatif",
    3: "Neutre",
    4: "Positif",
    5: "Positif fort"
}

# Appliquer le mapping à la colonne Predicted Sentiment
df["Sentiment Description"] = df["Predicted Sentiment"].map(mapping)

# Exporter le DataFrame en fichier CSV
output_file = "../prediction/sentiments_mappés.csv"

df.to_csv(
    'sentiments_mappés.csv',
    index=False,
    encoding='utf-8',
    sep=";",  # Utiliser ; comme séparateur
    quoting=csv.QUOTE_NONE,  # Désactiver les guillemets automatiques
    escapechar="\\",
    lineterminator='\n'  # Assurer une bonne gestion des retours à la ligne
)