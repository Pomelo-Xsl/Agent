from langchain_community.embeddings import DashScopeEmbeddings

# 需要向量化的文本
user_query = "特朗普上一次访华是什么时候？"
# 创建嵌入模型对象
embedding_model = DashScopeEmbeddings(model="text-embedding-v1")
# 向量化：将 user_query 转化成向量
vector = embedding_model.embed_query(user_query)

print(vector)
print(len(vector))