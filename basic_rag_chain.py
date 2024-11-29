from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os

load_dotenv()

def create_basic_rag_chain():
    """
    创建基础的RAG检索链
    """
    # 1. 加载向量存储
    embeddings = DashScopeEmbeddings(
        model="text-embedding-v1",
        dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
    )
    vector_store = FAISS.load_local(
        "knowledge_base/vector_store",
        embeddings,
        allow_dangerous_deserialization=True
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # 2. 创建提示模板
    template = """你是甜品日记蛋糕店的客服助手。
    请根据以下上下文信息，用专业且友善的语气回答客户的问题。
    如果上下文中没有相关信息，请说"抱歉，我没有这个信息"。

    上下��信息：
    {context}

    客户问题：{question}

    回答："""

    prompt = ChatPromptTemplate.from_template(template)

    # 3. 创建语言模型
    model = ChatOpenAI(
        temperature=0.7,
        model="deepseek-chat",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://api.deepseek.com/v1"
    )

    # 4. 构建RAG链
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

    return chain

if __name__ == "__main__":
    # 测试代码
    rag_chain = create_basic_rag_chain()
    
    # 测试问题列表
    test_questions = [
        "黑森林蛋糕的价格是多少？",
        "你们的蛋糕保质期是多久？",
        "可以提前多久预订蛋糕？"
    ]
    
    # 执行测试
    print("开始测试RAG链...\n")
    for question in test_questions:
        print(f"问题: {question}")
        response = rag_chain.invoke(question)
        print(f"回答: {response}\n") 