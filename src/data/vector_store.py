"""
向量存储模块
作者: 越山
"""
import logging
import shutil
from pathlib import Path
from typing import List, Optional, Union
import os
from langchain.schema import Document
from dashscope import TextEmbedding
from langchain.embeddings import DashScopeEmbeddings
from langchain.vectorstores import FAISS
from ..utils.config import config

logger = logging.getLogger(__name__)

class VectorStore:
    """向量存储管理类"""
    
    def __init__(self):
        # 设置 DashScope API Key
        os.environ["DASHSCOPE_API_KEY"] = config.dashscope_api_key
        
        # 初始化 embeddings
        self.embeddings = DashScopeEmbeddings(
            model="text-embedding-v2",
            dashscope_api_key=config.dashscope_api_key,
        )
        self.vector_store: Optional[FAISS] = None
        self.vector_store_path = config.vector_store_path
    
    def create_vector_store(self, documents: List[Document]) -> None:
        """创建向量存储"""
        logger.info("Creating new vector store...")
        self.vector_store = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )
        
        # 确保向量存储目录存在
        self.vector_store_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 保存向量存储
        self.save_vector_store()
        logger.info(f"Vector store created and saved to {self.vector_store_path}")
    
    def load_vector_store(self) -> bool:
        """加载向量存储"""
        if not self.vector_store_path.exists():
            logger.info("No existing vector store found.")
            return False
            
        try:
            logger.info(f"Loading vector store from {self.vector_store_path}")
            self.vector_store = FAISS.load_local(
                folder_path=str(self.vector_store_path),
                embeddings=self.embeddings,
                allow_dangerous_deserialization=True
            )
            logger.info("Vector store loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
            # 如果加载失败，删除可能损坏的向量存储文件
            if self.vector_store_path.exists():
                shutil.rmtree(self.vector_store_path)
                logger.info("Removed corrupted vector store")
            return False
    
    def save_vector_store(self) -> None:
        """保存向量存储"""
        if self.vector_store:
            logger.info(f"Saving vector store to {self.vector_store_path}")
            self.vector_store.save_local(str(self.vector_store_path))
    
    def similarity_search(self, query: Union[str, List[str]], k: int = 4) -> List[Document]:
        """相似度搜索"""
        if not self.vector_store:
            raise ValueError("Vector store not initialized")
        
        try:
            # DashScope需要数组形式的输入
            if isinstance(query, str):
                query_text = [query]
            else:
                query_text = query
            
            # 调用embeddings进行向量化
            embeddings = self.embeddings.embed_documents(query_text)
            
            # 使用向量进行搜索
            return self.vector_store.similarity_search_by_vector(
                embedding=embeddings[0],  # 使用第一个查询的向量
                k=k
            )
        except Exception as e:
            logger.error(f"Error in similarity search: {str(e)}")
            return []