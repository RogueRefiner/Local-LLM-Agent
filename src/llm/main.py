import ollama
from ollama import chat

content = """
"""

response = chat(
    model="qwen2.5-coder:7b",
    messages=[{"role": "user", "content": content}],
    stream=True,
)

for chunk in response:
    print(chunk.message.content, end="", flush=True)
