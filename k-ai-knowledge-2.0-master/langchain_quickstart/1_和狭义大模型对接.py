from langchain_community.llms.tongyi import Tongyi

# 1.创建模型的客户端
# 之前我们使用的是 qwen3-max,但是qwen3-max是聊天模型，不是狭义的llms
# qwen-max 是狭义的llms，适合于单次调用
llm = Tongyi(model="qwen-max")

# 2.调用模型
result = llm.invoke(input="你是谁？")

# 3.处理输出
print(type(result)) # <class 'str'>
print(result) # 我是Qwen，由阿里云开发的超大规模语言模型。我的目标是...