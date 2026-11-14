from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

# 1.创建对象
memory = InMemoryChatMessageHistory()

# 2.添加消息
memory.add_message(HumanMessage("你是谁?"))
memory.add_message(AIMessage("我是AI。"))

# 3.获取消息列表
print(memory.messages)