from itertools import chain

from langchain_community.llms.tongyi import Tongyi
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate

chat_prompt_template = ChatPromptTemplate.from_messages([
    ("system", "假设你是一个{expert}专家"),
    # SystemMessage(content="假设你是一个{expert}专家"),
    ("human", "什么是{user_input}")
    # HumanMessage(content="什么是{user_input}")
])
# prompt = chat_prompt_template.format(expert="AI", user_input="Langgraph")
# print(type(prompt)) # <class 'str'>
# print(prompt) # System: 假设你是一个AI专家 Human: 什么是Langgraph

prompt = chat_prompt_template.invoke(input={"expert": "AI", "user_input": "Langgraph"}).to_string()
print(type(prompt)) # <class 'str'>
print(prompt) # System: 假设你是一个AI专家 Human: 什么是Langgraph

# llm = Tongyi(model="qwen-max")
# chain = chat_prompt_template | llm
# result = chain.stream(input={"expert": "AI", "user_input": "Langgraph"})
# for chunk in result:
#     print(chunk, end='', flush=True)
