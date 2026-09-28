import requests


def search_products(query):
    search_url = "https://dummyjson.com/products/search"
    search_params = {
        "q": query,
        "limit": 5,
        "select": "title,price,rating,brand,category,description",
    }

    search_response = requests.get(search_url, params=search_params)
    search_response.raise_for_status()

    result = search_response.json()["products"]
    # print("result=", result)
    return result


functions = {"search_products": search_products}

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Search the product catalog by keyword (e.g. phone, laptop, perfume).",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    }
]
