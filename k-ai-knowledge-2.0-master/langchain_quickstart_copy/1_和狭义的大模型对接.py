from langchain_community.llms.tongyi import Tongyi

# 1.创建模型客户端
# qwen3-max : 聊天模型
# qwen-max
llm = Tongyi(model="qwen-max")

# 2.调用模型
result = llm.invoke(input="你是谁？")

# 3.处理输出
print(type(result)) # <class 'str'>
print(result) # 我是Qwen，由阿里云开发的预训练语言模型。我的设计目的是帮助用户生成各种类型的