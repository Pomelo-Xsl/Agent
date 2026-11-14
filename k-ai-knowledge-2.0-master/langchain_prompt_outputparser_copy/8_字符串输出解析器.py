from langchain_community.llms.tongyi import Tongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("请解释一下{concept}的概念")
# llm = ChatTongyi(model="qwen3-max", streaming=True)
llm = Tongyi(model="qwen-max")

parser = StrOutputParser()
chain = prompt | llm | parser
res = chain.invoke(input={"concept": "Langchain"})
print(type(res)) # <class 'langchain_core.messages.ai.AIMessage'>
print(res)
# print(res.content) # content='LangChain 是一个开源框架，旨在简化基于大型语言模型（
# for chunk in chain.stream(input={"concept": "Langchain"}):
#     print(chunk.content, end='', flush=True)