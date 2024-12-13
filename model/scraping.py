import csv

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


            country_tag = card.find("div",class_="typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_detailsIcon__Fo_ua")
            country = country_tag.find("span").text.strip() if country_tag and country_tag.find("span") else None

            score_tag = card.find("div", class_="star-rating_starRating__4rrcf")
            score = score_tag.img['alt'] if score_tag and score_tag.img else None

            date_tag = card.find("time")
            published_date = date_tag['datetime'] if date_tag else None

            content_tag = card.find("p", {"data-service-review-text-typography": "true"})
            content = content_tag.text.strip() if content_tag else None



            reviews.append({

                "Pays": country,
                "Note": score,
                "Contenu de l'avis": content,
                "Date de publication": published_date,

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
df.to_csv("luggage_superstore_reviews.csv", index=False, sep=";", quoting=csv.QUOTE_NONE, escapechar='\\')
print("Scraping terminé. Les données sont enregistrées dans 'luggage_superstore_reviews.csv'.")

