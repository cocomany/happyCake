"""
Gradio Web界面
作者: 越山
"""
import gradio as gr
from ..chains.rag_chain import rag_chain
import logging
import sys

# 配置更详细的日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# 确保所有相关模块的日志级别都是 INFO
logging.getLogger('langchain').setLevel(logging.INFO)
logging.getLogger('chains').setLevel(logging.INFO)
logging.getLogger('data').setLevel(logging.INFO)

logger = logging.getLogger(__name__)

# 定义异步回调函数
def chat_response(message: str, history: list) -> tuple[list, str]:
    """处理聊天消息"""
    logger.info("=== chat_response 函数被调用 ===")
    logger.info(f"输入消息: {message}")
    logger.info(f"当前历史: {history}")
    
    try:
        # 确保消息不为空
        if not message or not message.strip():
            logger.warning("收到空消息")
            return history, ""
            
        response = rag_chain.answer_question(message)
        logger.info(f"RAG Chain 返回响应: {response}")
        
        # 更新对话历史
        new_history = history + [(message, response)]
        logger.info(f"更新后的历史: {new_history}")
        
        return new_history, ""
        
    except Exception as e:
        logger.error(f"处理消息时出错: {str(e)}", exc_info=True)
        return history + [(message, f"抱歉，处理您的问题时出现了错误: {str(e)}")], ""

# 创建Gradio界面
def create_demo() -> gr.Blocks:
    """创建Gradio演示界面"""
    
    with gr.Blocks(title="甜品日记AI客服", theme="soft") as demo:
        gr.Markdown("""
        # 🍰 甜品日记AI客服
        
        欢迎使用甜品日记AI客服系统！我可以帮您：
        - 了解蛋糕产品信息
        - 查询价格和规格
        - 了解订购流程
        - 解答常见问题
        """)
        
        chatbot = gr.Chatbot(
            label="对话历史",
            height=500,
            bubble_full_width=False
        )
        
        with gr.Row():
            msg = gr.Textbox(
                label="请输入您的问题",
                placeholder="例如：你们有什么款式的生日蛋糕？",
                lines=2,
                scale=4
            )
            submit = gr.Button("发送", scale=1)
        
        with gr.Row():
            clear = gr.ClearButton(
                components=[msg, chatbot], 
                value="清空对话",
                scale=1
            )
            
        gr.Examples(
            examples=[
                "你们有什么款式的生日蛋糕？",
                "蛋糕可以提前多久预订？",
                "你们使用的是什么原材料？",
                "可以定制特殊图案吗？"
            ],
            inputs=msg,
            label="示例问题"
        )

        # 绑定提交事件
        submit.click(
            fn=chat_response,
            inputs=[msg, chatbot],  # 传入消息和历史
            outputs=[chatbot, msg],  # 输出更新后的历史和清空的输入框
            api_name="chat"
        )
        
        msg.submit(
            fn=chat_response,
            inputs=[msg, chatbot],
            outputs=[chatbot, msg]
        )

    return demo

def main():
    """启动Gradio服务"""
    demo = create_demo()
    demo.queue()  # 启用队列处理
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,  # 禁用share
        debug=False
    )

if __name__ == "__main__":
    main() 