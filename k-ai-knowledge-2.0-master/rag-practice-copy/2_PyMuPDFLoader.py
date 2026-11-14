from langchain_community.document_loaders import PyMuPDFLoader

file_path = r'E:\python\k-ai-knowledge-2.0\rag-practice-copy\data\files\sample_document.pdf'

pdf_loader = PyMuPDFLoader(file_path=file_path)
# 1.load() 一次性加载所有文档
docs = pdf_loader.load()
# print(type(docs)) # <class 'list'>
# print(type(docs[0])) # <class 'langchain_core.documents.base.Document'>
# print(len(docs)) # 6
for doc in docs:
    print(f"内容：{doc.page_content[:100]}")
    print(f"元信息：{doc.metadata}")
    print()
