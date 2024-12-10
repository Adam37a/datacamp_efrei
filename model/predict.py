from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
text = "Good luggage"
inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
outputs = model(**inputs)
scores = torch.nn.functional.softmax(outputs.logits, dim=-1)

for i, score in enumerate(scores[0]):
    print(f"Star {i+1}: {score:.2f}")

predicted_class = torch.argmax(scores) + 1
print(f"Predicted Sentiment: {predicted_class}-Star")