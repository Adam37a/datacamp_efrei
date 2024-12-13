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

Vous pouvez les installer avec la commande suivante pour installer les bibliotheque backend :
```bash
pip install -r requirements.txt
```
Vous pouvez les installer avec la commande suivante pour installer les bibliotheque datavisualisation :
```bash
pip install -r ./model/streamlit/requirements.txt
```

# Scraping
Le script extrait les avis depuis le site Trustpilot.

Exécutez le script scraping.py :

```bash
python model/scraping.py
```
**Fonctionnalité principale** :

Récupérer les données des avis (note, contenu, date de publication) sur plusieurs pages du site.
Utilise requests pour envoyer des requêtes HTTP et BeautifulSoup pour analyser le contenu HTML.

**Sortie:**

***Fichier contenant les avis bruts.***
datacamp_efrei/scraping/scrapped_file.csv



# Cleaning
Le script de nettoyage les données extraites.

Exécutez le script de nettoyage cleaning.py

```bash
python model/cleaning.py
```

**Étapes principales :** 

Remplacement des codes pays par leurs noms complets à l’aide d’un dictionnaire.
Nettoyage des textes des avis (suppression des espaces superflus, des emojis, des fautes d’orthographe, etc.).
Conversion des notes en valeurs numériques et transformation des dates au format datetime.

**Sortie avec des données nettoyées et prêtes à être analysées :**

datacamp_efrei/data_cleaning/avis_transformes_4.csv 

# Prediction tockenizer
Ce script analyse les sentiments des avis.

executer le ficher :
```bash
python model/predict_tokenizer.py
```

**Fonctionnalité principale :**

Utilise le modèle pré-entraîné nlptown/bert-base-multilingual-uncased-sentiment pour prédire un score de sentiment pour chaque avis.
Associe le score à chaque ligne du fichier nettoyé.

**Sortie:**

***Fichier contenant les sentiments prédits.:***
datacamp_efrei/model/streamlit/luggage_predicted_review_tokenizer.csv 



# Prediction Pipeline 
Exécutez le script predict_pipeline.py pour effectuer la prédiction en ajoutant une étape de prétraitement.

executer le ficher :
```bash
python model/predict_pipeline.py
```
** Fonctionnalités supplémentaires : **

Mise en évidence de mots-clés positifs et négatifs.
Ajout des prédictions dans les données.
***Fichier contenant les sentiments prédits.:***
datacamp_efrei/model/streamlit/luggage_predicted_review_pipeline.csv


# Mapping
Ce script ajoute des descriptions textuelles aux sentiments numériques.

**Étapes principales :**

Associe chaque score de sentiment (1 à 5) à une description comme "Positif fort" ou "Négatif".
Ajoute ces descriptions dans une nouvelle colonne.
Sortie :

***Fichier sentiments_mappés.csv prêt pour analyse et visualisation.***
datacamp_efrei/model/streamlit/luggage_predicted_review_tokenizer.csv

# Évaluer les performances des modèles
### Analyse des prédictions du Tokenizer**
Exécutez le script matrice_confusion_tockenizer.py pour évaluer les performances du modèle basé sur le tokenizer.

```bash
python model/matrice_confusion_tockenizer.ipynb
```

*** Fonctionnalités : ***
Génération d’une matrice de confusion.
Calcul de métriques telles que la précision et le MSE.


### Analyse des prédictions du Pipeline
Exécutez le script matrice_confusion_pipeline.py pour évaluer les performances du pipeline de prédiction.

```bash
python matrice_confusion_pipeline.ipynb
```

*** Fonctionnalités : ***
Analyse similaire à celle du tokenizer.
Comparaison des notes réelles avec les sentiments prédits.



# Visualisations et Tableau de Bord
Ce projet inclut un tableau de bord interactif développé avec Streamlit pour visualiser et analyser les résultats obtenus. Le tableau de bord est accessible en ligne via le lien suivant :
**https://datacampefreisentimentanalysis.streamlit.app/**
Les explications des visualisations se trouvent dans le pdf de documentation du projet.



