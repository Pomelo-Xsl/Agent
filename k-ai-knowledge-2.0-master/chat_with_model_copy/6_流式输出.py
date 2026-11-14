import os
from openai import OpenAI

client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
              {'role': 'user', 'content': '你是谁？'}],
    stream=True,
    stream_options={"include_usage": True}
)

for chunk in completion:
    # print(chunk.model_dump_json())
    if chunk.choices:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end='', flush=True)
    elif hasattr(chunk, 'usage') and chunk.usage:
        print(f"\n\nToken使用情况: {chunk.usage}")
