from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat_prompt_template = ChatPromptTemplate.from_messages([
    ("system", "假设你是一个AI专家"),
    MessagesPlaceholder("history"),
    ("human", "我刚才问了什么内容？"),
])

chat_history = [
    ("human", "什么是Langgraph"),
    ("ai", "LangGraph是一种将自然语言处理（NLP）与图神经网络（GNN, Graph Neural Networks）相结合的技术或方法。")
]

# text = chat_prompt_template.format(history=chat_history)
# print(type(text))
# print(text)
print(chat_prompt_template.invoke(input={"history": chat_history}).to_string())

# llm = ChatTongyi(model="qwen3-max")
# chain = chat_prompt_template | llm
# result = chain.invoke(input={"history": chat_history})
#
# print(type(result)) # <class 'langchain_core.messages.ai.AIMessage'>
# print(result) # content='你刚才问的是：“什么是Langgraph”。' additional_kwargs={} res
# print(result.content) # 你刚才问的是：“什么是Langgraph”。