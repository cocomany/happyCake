"""
RAG链实现模块
作者: 越山
"""
from typing import List, Dict, Any
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.runnable.base import RunnableParallel
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema.messages import AIMessage, HumanMessage
from ..data.document_loader import DocumentLoader
from ..data.vector_store import VectorStore
from ..utils.config import config
import logging

# 系统提示词
SYSTEM_TEMPLATE = """你是甜品日记蛋糕店的AI客服助手。请根据提供的上下文信息和对话历史，以专业、友善的态度回答客户的问题。
如果问题超出上下文范围，请礼貌地告知客户你只能回答与甜品日记产品和服务相关的问题。

上下文信息:
{context}

对话历史:
{history}

当前问题: {question}

请记住：
1. 回答要简洁明了
2. 态度要亲切友好
3. 不要编造不在上下文中的信息
4. 如果不确定，要诚实地说不知道
"""

logger = logging.getLogger(__name__)

class RAGChain:
    """RAG链实现类"""
    
    def __init__(self):
        # 初始化组件
        self.document_loader = DocumentLoader()
        self.vector_store = VectorStore()
        self.llm = ChatOpenAI(
            model_name=config.model_name,
            openai_api_key=config.openai_api_key,
            openai_api_base=config.openai_api_base,
            temperature=0.7,
            streaming=True
        )
        
        # 初始化对话记忆
        self.memory = ConversationBufferMemory(
            memory_key="history",
            return_messages=True
        )
        
        # 初始化知识库
        self._initialize_knowledge_base()
        
        # 创建提示词模板
        self.prompt = ChatPromptTemplate.from_template(SYSTEM_TEMPLATE)
        
        # 构建RAG链
        self.chain = (
            RunnableParallel(
                {
                    "context": self._get_context, 
                    "question": RunnablePassthrough(),
                    "history": self._get_history
                }
            )
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
    
    def _get_history(self, _: str) -> str:
        """获取对话历史"""
        try:
            memory_variables = self.memory.load_memory_variables({})
            history = memory_variables.get("history", "")
            return str(history)
        except Exception as e:
            logger.error(f"Error loading history: {e}")
            return ""
    
    def _initialize_knowledge_base(self) -> None:
        """初始化知识库"""
        try:
            # 尝试加载已有的向量存储
            if not self.vector_store.load_vector_store():
                # 如果加载失败，则重新创建
                documents = self.document_loader.load_documents()
                if not documents:
                    raise ValueError("No documents found in knowledge base")
                self.vector_store.create_vector_store(documents)
        except Exception as e:
            logger.error(f"Failed to initialize knowledge base: {str(e)}")
            raise RuntimeError(f"Failed to initialize knowledge base: {str(e)}")
    
    def _get_context(self, question: str) -> str:
        """获取相关上下文"""
        try:
            # 执行相似度搜索
            relevant_docs = self.vector_store.similarity_search(question)
            if not relevant_docs:
                return "抱歉，我没有找到相关的信息。请您换个方式提问，或者询问其他问题。"
            
            # 将文档内容合并为上下文字符串
            context = "\n\n".join(doc.page_content for doc in relevant_docs)
            logger.info(f"找到相关上下文: {context[:200]}...")  # 只记录前200个字符
            return context
            
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            return "抱歉，在检索相关信息时遇到了问题。请稍后再试。"
    
    async def answer_question(self, question: str) -> str:
        """处理用户问题并返回答案"""
        if not question.strip():
            return "请输入您的问题。"
            
        try:
            logger.info(f"开始处理问题: {question}")
            
            # 生成回答
            response = await self.chain.ainvoke(question)
            logger.info(f"生成回答: {response}")
            
            # 保存对话历史
            self.memory.save_context(
                {"input": question},
                {"output": response}
            )
            
            return response
            
        except Exception as e:
            logger.error(f"处理问题时出错: {str(e)}", exc_info=True)
            return f"抱歉，处理您的问题时出现了错误: {str(e)}"

# 创建全局RAG链实例
rag_chain = RAGChain() 