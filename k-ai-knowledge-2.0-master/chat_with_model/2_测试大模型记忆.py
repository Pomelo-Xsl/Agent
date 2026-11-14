from openai import OpenAI

# 1.创建客户端对象
client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 2. 第一次调用：告诉模型用户身份
completion = client.chat.completions.create(
    model="qwen3-max",
    messages=[
        {"role": "user", "content": "你好，我是阿苑，是一个AI老师。"},
    ]
)
print(completion.model_dump_json())

# 3. 第二次调用：询问模型“我是谁？”
completion = client.chat.completions.create(
    model="qwen3-max",
    messages=[
        {"role": "user", "content": "我是谁？"},
    ]
)
print(completion.model_dump_json())
# print(completion.choices[0].message.content)
