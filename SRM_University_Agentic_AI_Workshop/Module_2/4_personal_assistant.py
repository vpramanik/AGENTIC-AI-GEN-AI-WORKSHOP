import os
import json
import importlib
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

# importing from 4_agent_tools.py to keep this file short and readable
tools_module = importlib.import_module("4_agent_tools")
functions = tools_module.functions
tools = tools_module.tools

messages = [
    {
        "role": "system",
        "content": "You are a helpful shopping assistant. Always use the available tools to search for products. Don't add any text formatting.",
    }
]

print("\nTry this:\nAsk for mobile\nAsk for fruits\nAsk, what options do I have to eat?\nAsk for apple\n\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ("exit", "quit"):
        break

    messages.append({"role": "user", "content": user_input})

    while True:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=tools,
        )
        message = completion.choices[0].message
        
        # print("🟡 : message:", message)

        messages.append(message)

        if not message.tool_calls:
            break

        for call in message.tool_calls:
            args = json.loads(call.function.arguments)
            print("\n------- --------------- -------")
            result = functions[call.function.name](**args)
            print(f"[tool] {call.function.name}({args}) = {result}")
            print("------- --------------- -------\n")

            messages.append({"role": "tool", "tool_call_id": call.id, "content": str(result)})

    print(f"Assistant: {message.content}\n")
