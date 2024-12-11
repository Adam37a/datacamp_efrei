import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os
import shutil

model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
input_file_path = r"C:\Users\ahana\Desktop\ML_datacamp\datacamp_efrei\data_cleaning\avis_transformes_4.csv"
output_folder = r"datacamp_efrei\prediction"
os.makedirs(output_folder, exist_ok=True)
duplicated_file_path = os.path.join(output_folder, "luggage_superstore_reviews.csv")
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
