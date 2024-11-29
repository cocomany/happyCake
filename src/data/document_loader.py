"""
文档加载和处理模块
作者: 越山
"""
from pathlib import Path
from typing import List
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ..utils.helpers import get_all_markdown_files, read_markdown_file
from ..utils.config import config

class DocumentLoader:
    """文档加载器类"""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?"]
        )
    
    def load_documents(self) -> List[Document]:
        """加载并处理知识库文档"""
        documents = []
        
        # 获取所有Markdown文件
        markdown_files = get_all_markdown_files(config.knowledge_base_path)
        
        # 处理每个文件
        for file_path in markdown_files:
            # 读取文件内容
            content = read_markdown_file(file_path)
            if not content:
                continue
                
            # 获取相对路径作为元数据
            relative_path = file_path.relative_to(config.knowledge_base_path)
            
            # 创建文档对象
            doc = Document(
                page_content=content,
                metadata={
                    "source": str(relative_path),
                    "file_path": str(file_path)
                }
            )
            documents.append(doc)
        
        # 分割文档
        split_docs = self.text_splitter.split_documents(documents)
        
        return split_docs

    def process_query(self, query: str) -> List[Document]:
        """处理用户查询文本"""
        return self.text_splitter.create_documents([query]) 