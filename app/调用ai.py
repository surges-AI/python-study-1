import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {"role": "system", "content": "你是一个非常可爱的智能对话ai"},
        {"role": "user", "content": "你好"},
    ],
    stream=False,
)

print(response.choices[0].message.content)