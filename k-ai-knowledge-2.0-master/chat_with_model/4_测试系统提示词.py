from openai import OpenAI

# 1.创建客户端对象
client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 2. 第一次调用：告诉模型用户身份
completion = client.chat.completions.create(
    model="qwen3-max",
    messages=[
        {"role": "system", "content": "背景设定：你现在是一个AI老师，负责上AI课程。"},
        {"role": "user", "content": "你是谁？"},
    ]
)
print(completion.choices[0].message.content)
