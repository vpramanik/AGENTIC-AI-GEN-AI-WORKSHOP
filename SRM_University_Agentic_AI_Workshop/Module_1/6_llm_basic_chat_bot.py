import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

while True:
    user_input = input("You: ")
    if user_input.lower() in ("exit", "quit"):
        break

    message = [{"role": "user", "content": user_input}]

    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct:novita",
        messages=message,
    )

    reply = completion.choices[0].message.content
    print(f"Assistant: {reply}\n")
