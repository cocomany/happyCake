from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import FAISS
import os
from dotenv import load_dotenv
from glob import glob

load_dotenv()

def load_and_process_documents():
    """
    加载知识库文档并创建向量存储
    """
    documents = []
    
    # 1. 加载所有.md文件
    for file_path in glob("knowledge_base/**/*.md", recursive=True):
        try:
            loader = TextLoader(file_path, encoding='utf-8')
            documents.extend(loader.load())
            print(f"Loaded: {file_path}")
        except Exception as e:
            print(f"Error loading {file_path}: {str(e)}")
    
    print(f"\nLoaded {len(documents)} documents")

    # 2. 文档分割
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    texts = text_splitter.split_documents(documents)
    print(f"Split into {len(texts)} chunks")

    # 3. 创建向量存储
    embeddings = DashScopeEmbeddings(
        model="text-embedding-v1",
        dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
    )
    
    vector_store = FAISS.from_documents(texts, embeddings)
    
    # 4. 保存向量存储
    vector_store.save_local("knowledge_base/vector_store")
    print("Vector store saved successfully")
    
    return vector_store

if __name__ == "__main__":
    # 测试代码
    vector_store = load_and_process_documents()
    
    # 测试检索
    query = "黑森林蛋糕多少钱？"
    docs = vector_store.similarity_search(query, k=2)
    
    print("\nTest Query:", query)
    print("\nRetrieved documents:")
    for i, doc in enumerate(docs, 1):
        print(f"\n{i}. {doc.page_content[:200]}...") 