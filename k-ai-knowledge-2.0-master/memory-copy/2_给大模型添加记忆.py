from langchain_community.chat_models import ChatTongyi

# 1. 创建通义千问客户端（选择 qwen3-max 模型）
llm = ChatTongyi(model="qwen3-max")

# 2. 定义对话历史
chat_history = []

# 3. 第一次调用：用户自我介绍
user_message_1 = "你好，我是阿苑，是一个AI老师"
chat_history.append(("user", user_message_1))

ai_reply_1 = llm.invoke(user_message_1)
chat_history.append(("ai", ai_reply_1))
print("第一次AI回复：", ai_reply_1)


# 4. 第二次调用：询问“我是谁？”—— 携带完整历史
user_message_2 = "我是谁？"
context_messages = chat_history + [("user", user_message_2)]
context_text = "\n".join([f"{role}: {msg}" for role, msg in context_messages])
print()
print(context_text)
print()
ai_reply_2 = llm.invoke(context_text)
chat_history.append(("ai", ai_reply_2))
print("第二次AI回复：", ai_reply_2)






