import json
import requests
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

response = requests.get(
    "https://dummyjson.com/products",
    params={"limit": 0, "select": "title,price,description"},
)
response.raise_for_status()
products = response.json()["products"]

for product in products:
    text = f"{product['title']}. {product['description']}"
    product["embedding"] = model.encode(text).tolist()

with open("4_products.json", "w") as f:
    json.dump(products, f)

print(f"Saved {len(products)} products to 4_products.json")
