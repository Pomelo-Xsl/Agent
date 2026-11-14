from langchain_community.document_loaders import TextLoader

file_path = r'E:\python\k-ai-knowledge-2.0\rag-practice-copy\data\files\北京有什么好玩的.txt'

# 加载文本文件
text_loader = TextLoader(file_path, encoding="utf-8")
docs = text_loader.load() # List[Document]
print(type(docs))
print(f"加载了 {len(docs)} 个文档")
print(f"内容: {docs[0].page_content}...")
print(f"元数据: {docs[0].metadata}")