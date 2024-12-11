import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def scrape_reviews(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, "html.parser")

    reviews = []

    review_cards = soup.find_all("div", class_="styles_cardWrapper__LcCPA")

    for card in review_cards:
        try:
            # Nom de l'utilisateur
            #name_tag = card.find("span", {"data-consumer-name-typography": "true"})
           # name = name_tag.text.strip() if name_tag else None

            # Nombre d'avis de l'utilisateur
            #review_count_tag = card.find("span", {"data-consumer-reviews-count-typography": "true"})
           # review_count = review_count_tag.text.strip() if review_count_tag else None

            # Note de l'avis
            score_tag = card.find("div", class_="star-rating_starRating__4rrcf")
            score = score_tag.img['alt'] if score_tag and score_tag.img else None

            # Date de publication
            date_tag = card.find("time")
            published_date = date_tag['datetime'] if date_tag else None

            # Contenu de l'avis
            content_tag = card.find("p", {"data-service-review-text-typography": "true"})
            content = content_tag.text.strip() if content_tag else None

            # Réponse de l'entreprise (si présente)
            #reply_tag = card.find("p", {"data-service-review-business-reply-text-typography": "true"})
            #reply = reply_tag.text.strip() if reply_tag else None

            # Ajoute les données extraites à la liste
            reviews.append({
                #"Nom": name,
                #"Nombre d'avis": review_count,
                "Note": score,
                "Date de publication": published_date,
                "Contenu de l'avis": content,
                #"Réponse de l'entreprise": reply
            })
        except Exception as e:
            print(f"Erreur lors de l'extraction d'un avis : {e}")

    return reviews



base_url = "https://fr.trustpilot.com/review/luggagesuperstore.co.uk?page="
all_reviews = []


for page in range(1, 78):
    print(f"Scraping page {page}")
    page_url = f"{base_url}{page}"
    all_reviews.extend(scrape_reviews(page_url))
    time.sleep(2)

df = pd.DataFrame(all_reviews)
df.to_csv("luggage_superstore_reviews.csv", index=False)
print("Scraping terminé. Les données sont enregistrées dans 'luggage_superstore_reviews.csv'.")
