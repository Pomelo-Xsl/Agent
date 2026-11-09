from langchain_community.chat_models import ChatTongyi
from langchain_community.llms.tongyi import Tongyi

# 创建模型客户端-调用大模型-处理输出

llm = ChatTongyi(model='deepseek-v4-pro-0813')

result = llm.invoke(input='你是谁？')

print(type(result))
print(result)