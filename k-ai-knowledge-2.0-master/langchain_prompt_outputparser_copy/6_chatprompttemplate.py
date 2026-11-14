from langchain_community.chat_models import ChatTongyi
from langchain_community.llms.tongyi import Tongyi
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


chat_prompt_template = ChatPromptTemplate.from_messages([
    ("system", "假设你是一个{expert}专家"),
    ("human", "请你解释一下{content}是什么。")
])

# prompt = chat_prompt_template.format(expert="AI", content="Langgraph")
# print(type(prompt))
# print(prompt)
# prompt = chat_prompt_template.invoke(input={"expert": "AI", "content": "Langgraph"}).to_string()
# print(type(prompt))
# print(prompt)

llm = ChatTongyi(model="qwen3-max", streaming=True)
chain = chat_prompt_template | llm
result = chain.stream(input={"expert": "AI", "content": "Langgraph"})
for chunk in result:
    print(chunk.content, end='', flush=True)