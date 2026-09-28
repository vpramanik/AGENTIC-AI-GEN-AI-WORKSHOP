import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

# ORIGINAL (fails when running from outside Module_2 directory):
# with open("4_products.json") as f:
# NEW (resolves path relative to this script's location):
_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(_dir, "4_products.json")) as f:
    products = json.load(f)


def dot_product(a, b):
    return np.dot(a, b)


def cosine_similarity(a, b):
    return dot_product(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def euclidean(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))


def manhattan(a, b):
    return np.sum(np.abs(np.array(a) - np.array(b)))


def semantic_search(query):
    query_embedding = model.encode(query)

    scored = []
    for product in products:
        score = cosine_similarity(query_embedding, product["embedding"])
        # score = dot_product(query_embedding, product["embedding"])
        # score = euclidean(query_embedding, product["embedding"])
        # score = manhattan(query_embedding, product["embedding"])
        scored.append((score, product))

    scored.sort(key=lambda item: item[0], reverse=True)

    result = []
    for score, product in scored[:5]:
        result.append({
            "title": product["title"],
            "price": product["price"],
            "description": product["description"],
            "score": round(float(score), 3),
        })
    return result


functions = {"semantic_search": semantic_search}

tools = [
    {
        "type": "function",
        "function": {
            "name": "semantic_search",
            "description": "Find products that match what the user is looking for, by meaning (e.g. 'something to keep my coffee hot').",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    }
]
