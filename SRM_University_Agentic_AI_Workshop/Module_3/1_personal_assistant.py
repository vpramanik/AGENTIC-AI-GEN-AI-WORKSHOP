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

# importing from 1_agent_tools.py to keep this file short and readable
tools_module = importlib.import_module("1_agent_tools")
functions = tools_module.functions
tools = tools_module.tools

messages = [
    {
        "role": "system",
        "content": "You are a helpful email assistant. Use the available tools to read and send emails. Before sending, write a clear subject and body. Don't add any text formatting.",
    }
]

print("\nTry this:\nRead my latest 3 emails\nSummarise my inbox\nSend an email to friend@example.com saying I will be late\n\n")

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
