from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate

# 1.创建模型的客户端
llm = Tongyi(model="qwen-max")

# 2.调用模型
prompt_template = PromptTemplate.from_template(
    "假设你是一个{expert}专家，请你解释一下{content}是什么。"
)
prompt = prompt_template.format(expert="AI", content="Langgraph")
# print(type(prompt))
# print(prompt)
result = llm.stream(input=prompt)

# 3.处理输出
for chunk in result:
    print(chunk, end='', flush=True)