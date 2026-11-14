from langchain_community.chat_models import ChatTongyi
from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat_prompt_template = ChatPromptTemplate.from_messages([
    ("system", "假设你一个AI专家"),
    MessagesPlaceholder("history"),
    ("human", "我刚才问了什么内容")
])

chat_history = [
    ("human", "什么是Langgraph"),
    ("ai", "LangGraph是一种结合了自然语言处理（NLP）和图数据库技术的框架或方法论，旨在通过将文本信息转化为结构化的图数据来提高对复杂文本的理解与分析能力。")
]

# result = chat_prompt_template.format(history=chat_history)
# print(type(result))
# print(result)
# print(chat_prompt_template.invoke(input={"history": chat_history}).to_string())
#
# llm = Tongyi(model="qwen-max") # todo: coding fixed
# # llm = ChatTongyi(model="qwen3-max", streaming=True)
# chain = chat_prompt_template | llm
# result = chain.stream(input={"history": chat_history})
# for chunk in result:
#     # print(chunk.content, end='', flush=True)
#     print(chunk, end='', flush=True)



