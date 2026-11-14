import os
from openai import OpenAI

# 1.创建[模型]客户端对象
client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 2.调用模型 5c
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁？"},
    ]
)

# 3.打印输出
print(completion.model_dump_json())
# 3.1. 只打印内容，不打印别的信息
print(completion.choices[0].message.content)