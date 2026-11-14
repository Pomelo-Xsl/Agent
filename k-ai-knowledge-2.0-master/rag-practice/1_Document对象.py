from langchain_core.documents import Document

# 手动创建 Document 对象
doc = Document(
    page_content="这是文档的正文内容。",
    metadata={"source": "example.txt", "page": 1}
)

print(doc.page_content)  # 输出: 这是文档的正文内容。
print(doc.metadata)      # 输出: {'source': 'example.txt', 'page': 1}