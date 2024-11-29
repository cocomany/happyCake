"""
命令行聊天界面
作者: 越山
"""
import asyncio
from ..chains.rag_chain import rag_chain

async def chat_loop():
    """聊天循环"""
    print("欢迎使用甜品日记AI客服系统！输入 'quit' 或 'exit' 退出。")
    print("请输入您的问题:")
    
    while True:
        # 获取用户输入
        user_input = input("\n> ").strip()
        
        # 检查是否退出
        if user_input.lower() in ['quit', 'exit']:
            print("\n感谢使用，再见！")
            break
            
        if not user_input:
            continue
            
        # 获取回答
        try:
            response = await rag_chain.answer_question(user_input)
            print(f"\nAI助手: {response}")
        except Exception as e:
            print(f"\n发生错误: {str(e)}")

def main():
    """主函数"""
    try:
        asyncio.run(chat_loop())
    except KeyboardInterrupt:
        print("\n\n程序已终止。感谢使用！")
    except Exception as e:
        print(f"\n程序发生错误: {str(e)}")

if __name__ == "__main__":
    main() 