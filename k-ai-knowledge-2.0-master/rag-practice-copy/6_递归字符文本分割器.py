from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

file_path = r'E:\python\k-ai-knowledge-2.0\rag-practice-copy\data\files\历史文化.txt'
# 1.加载文档
loader = TextLoader(file_path=file_path, encoding='utf-8')
docs = loader.load()

# 2.文本拆分
splitter = RecursiveCharacterTextSplitter(
    chunk_size=55,
    chunk_overlap=8,
    separators=["\n\n", "\n", "。", "，", "、", " ", ""],
    length_function=len
)
chunks = splitter.split_text(docs[0].page_content)
for i, chunk in enumerate(chunks):
    print(f"--- 块 {i + 1} (长度: {len(chunk)}) ---")
    print(chunk)
    print()