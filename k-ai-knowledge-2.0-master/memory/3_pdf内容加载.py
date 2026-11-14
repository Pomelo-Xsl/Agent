from langchain_community.document_loaders import PyMuPDFLoader

file_path = "E:\python\k-ai-knowledge-2.0\memory\data\sample_document.pdf"
# 1.获取PDF文档内容
docs = PyMuPDFLoader(file_path).load()
# 2. 打印PDF文档内容
for doc in docs:
    print(doc.page_content)