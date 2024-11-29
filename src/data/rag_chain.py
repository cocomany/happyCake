"""
RAG链实现模块
作者: 越山
"""
from typing import List, Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from ..data.document_loader import DocumentLoader
from ..data.vector_store import VectorStore
from ..utils.config import config 