import gradio as gr
from basic_rag_chain import create_basic_rag_chain
import os
from dotenv import load_dotenv

load_dotenv()

def create_gradio_demo():
    """
    创建一个简单可靠的Gradio聊天界面
    """
    # 初始化RAG链
    try:
        rag_chain = create_basic_rag_chain()
        print("RAG链初始化成功！")
    except Exception as e:
        print(f"RAG链初始化失败: {str(e)}")
        raise e

    with gr.Blocks() as demo:
        # 添加标题和说明
        gr.Markdown("""
        # 🍰 甜品日记AI客服
        欢迎咨询蛋糕相关问题！
        """)
        
        # 创建聊天组件
        chatbot = gr.Chatbot(height=400)
        msg = gr.Textbox(label="请输入您的问题", placeholder="例如：黑森林蛋糕多少钱？")
        clear = gr.Button("清除对话")
        
        # 示例问题
        gr.Examples(
            examples=[
                "黑森林蛋糕多少钱？",
                "蛋糕可以提前多久预订？",
                "你们的蛋糕保质期是多久？",
                "草莓奶油蛋糕有什么规格？"
            ],
            inputs=msg,
            label="示例问题"
        )

        def user(user_message, history):
            """处理用户输入"""
            return "", history + [[user_message, None]]

        def bot(history):
            """处理AI响应"""
            try:
                response = rag_chain.invoke(history[-1][0])
                history[-1][1] = response
                return history
            except Exception as e:
                history[-1][1] = f"抱歉，系统出现错误: {str(e)}"
                return history

        def clear_history():
            """清除对话历史"""
            return None

        # 设置事件处理
        msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
            bot, chatbot, chatbot
        )
        clear.click(clear_history, None, chatbot)

    return demo

if __name__ == "__main__":
    # 确保环境变量已加载
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("请确保设置了 OPENAI_API_KEY 环境变量")
    
    if not os.getenv("DASHSCOPE_API_KEY"):
        raise ValueError("请确保设置了 DASHSCOPE_API_KEY 环境变量")
    
    # 创建并启动界面
    demo = create_gradio_demo()
    demo.queue()  # 启用队列模式
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        debug=True
    ) 