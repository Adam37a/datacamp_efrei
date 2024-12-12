import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os
import shutil
import csv
import numpy

model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
input_file_path = r"datacamp_efrei\data_cleaning\avis_transformes_4.csv"
output_folder = r"datacamp_efrei\prediction"
os.makedirs(output_folder, exist_ok=True)
duplicated_file_path = os.path.join(output_folder, "luggage_predicted_review_for_analysis.csv")
shutil.copy(input_file_path, duplicated_file_path)
df = pd.read_csv(duplicated_file_path, encoding='utf-8', delimiter=';')

if "Contenu de l'avis" not in df.columns:
    raise KeyError("Column 'Contenu de l'avis' not found in the dataset.")

predictions = []

for index, row in df.iterrows():
    text = str(row["Contenu de l'avis"])
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    scores = torch.nn.functional.softmax(outputs.logits, dim=-1)
    predicted_class = torch.argmax(scores) + 1
    predictions.append(predicted_class.item())

df['Predicted Sentiment'] = predictions
df.to_csv(duplicated_file_path, index=False)

print(f"Processed file saved to {duplicated_file_path}")


df = pd.read_csv(duplicated_file_path, encoding='utf-8', delimiter=';')

mapping = {
    1: "Très négatif",
    2: "Négatif",
    3: "Neutre",
    4: "Positif",
    5: "Très positif"
}

df["Sentiment Description"] = df["Predicted Sentiment"].map(mapping)

output_file = "../prediction/sentiments_mappés_output_final.csv"

df.to_csv(
    'sentiments_mappés.csv',
    index=False,
    encoding='utf-8',
    sep=";",
    quoting=csv.QUOTE_NONE,
    escapechar="\\",
    lineterminator='\n'
)

shutil.copy(duplicated_file_path,r"datacamp_efrei\model\streamlit\sentiments_mappés_output_final.csv")