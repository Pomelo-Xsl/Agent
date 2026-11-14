from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# 1.创建 Chroma 客户端
chroma_db = Chroma(
    collection_name="test-collection-2",
    embedding_function=DashScopeEmbeddings(),
    persist_directory="./chroma_db",
    collection_metadata={"hnsw:space": "cosine"}  # 余弦相似度
)

# 2. 新增 document
data = [
    Document(page_content="猫坐在垫子上"),
    Document(page_content="一只猫在垫子上休息"),
    Document(page_content="今天天气很好")
]

chroma_db.add_documents(
    documents=data,
    ids=[f"id-{i}" for i in range(1, len(data) + 1)]
)

# 3.相似度查询（和mysql的 where 等值查询不一样，我们这里是基于相似度匹配）
user_query = "猫在哪？"
result = chroma_db.similarity_search_with_relevance_scores(user_query, k=3)
print(type(result))
print(result)