from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import SystemMessage, HumanMessage

# 1.创建模型客户端
llm = ChatTongyi(model="qwen3-max")

# 2. 准备上下文
chat_history = [
    SystemMessage(content="背景设定：你现在是一个AI老师，负责上AI课程。"),
    HumanMessage(content="你是谁?")
]

# 3.携带上下文去调用模型
result= llm.invoke(input=chat_history)

# 4.处理输出
# print(type(result)) # <class 'langchain_core.messages.ai.AIMessage'>
# print(result)
"""
content='内容' 
additional_kwargs={} 
response_metadata={
model_name': 'qwen3-max', 
'finish_reason': 'stop', 'request_id': 'b83221d7-5a8e-9773-b159-c26cf2ea4631', 
'token_usage': {'input_tokens': 29, 'output_tokens': 106,  'total_tokens': 135}}
id='lc_run--019eb097-e96f-7d42-b7c5-251a7773f3b2-0' tool_calls=[] invalid_tool_calls=[]
"""
print(result.content)









