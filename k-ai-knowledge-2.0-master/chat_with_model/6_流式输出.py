import os
from openai import OpenAI

# 1.创建客户端对象
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 2. 和模型交互：开启流失输出
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': '你是谁？'}],
    stream=True, # 开启流式输出
    # stream_options={"include_usage": True}
    )

# 3. 按照chunk输出内容
for chunk in completion:
    print(chunk.model_dump_json())
    # print(chunk.choices[0].delta.content, end='', flush=True)