# DATACAMP PROJECT

Ce projet extrait des avis trustpilot de l'entreprise "Luggage Superstore" , nettoie les données, analyse les sentiments des commentaires et mappe les résultats pour produire un fichier final. Voici les instructions pour exécuter les différents scripts afin de reproduire les résultats.

## Prérequis

Assurez-vous d'avoir installé les bibliothèques Python suivantes :
- `requests`
- `beautifulsoup4`
- `pandas`
- `textblob`
- `emoji`
- `transformers`
- `torch`

Vous pouvez les installer avec la commande suivante :
```bash
pip install -r requirements.txt
```


# Scraping
Le script extrait les avis depuis le site Trustpilot.

**Fonctionnalité principale** :

Récupérer les données des avis (note, contenu, date de publication) sur plusieurs pages du site.
Utilise requests pour envoyer des requêtes HTTP et BeautifulSoup pour analyser le contenu HTML.

**Sortie:**

***Fichier luggage_superstore_reviews.csv contenant les avis bruts.***



# Cleaning
Le script de nettoyage les données extraites.

**Étapes principales :** 

Remplacement des codes pays par leurs noms complets à l’aide d’un dictionnaire.
Nettoyage des textes des avis (suppression des espaces superflus, des emojis, des fautes d’orthographe, etc.).
Conversion des notes en valeurs numériques et transformation des dates au format datetime.

**Sortie:**

***Fichier avis_transformes_4.csv avec des données nettoyées et prêtes à être analysées.***

# Prediction
Ce script analyse les sentiments des avis.

**Fonctionnalité principale :**

Utilise le modèle pré-entraîné nlptown/bert-base-multilingual-uncased-sentiment pour prédire un score de sentiment pour chaque avis.
Associe le score à chaque ligne du fichier nettoyé.

**Sortie:**

***Fichier luggage_predicted_review.csv contenant les sentiments prédits.***


# Mapping
Ce script ajoute des descriptions textuelles aux sentiments numériques.

**Étapes principales :**

Associe chaque score de sentiment (1 à 5) à une description comme "Positif fort" ou "Négatif".
Ajoute ces descriptions dans une nouvelle colonne.
Sortie :

***Fichier sentiments_mappés.csv prêt pour analyse et visualisation.***



# Visualisations et Tableau de Bord
Ce projet inclut un tableau de bord interactif développé avec Streamlit pour visualiser et analyser les résultats obtenus. Le tableau de bord est accessible en ligne via le lien suivant :
**https://datacampefreisentimentanalysis.streamlit.app/**




