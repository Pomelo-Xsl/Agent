from langchain_community.document_loaders import TextLoader

file_path = "E:\python\k-ai-knowledge-2.0\memory\data\北京有什么好玩的.txt"
# 1.获取TXT文档内容
docs = TextLoader(file_path, encoding="utf-8").load()
# 2. 打印TXT文档内容
for doc in docs:
    print(doc.page_content)
