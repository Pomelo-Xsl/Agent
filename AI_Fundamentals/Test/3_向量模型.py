from langchain_community.embeddings import DashScopeEmbeddings

#1、创建模型嵌入对象
embeding = DashScopeEmbeddings() #向量长度

#2、文本向量化
text = "内容"
vector = embeding.embed_query()

#3、处理输出
print()


