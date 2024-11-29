from basic_rag_chain import create_basic_rag_chain
import sys

def create_cli_interface():
    """
    创建命令行交互界面
    """
    # 初始化RAG链
    try:
        rag_chain = create_basic_rag_chain()
        print("系统初始化成功！")
    except Exception as e:
        print(f"系统初始化失败: {str(e)}")
        sys.exit(1)

    print("\n欢迎使用甜品日记AI客服系统")
    print("输入 'quit' 退出系统")

    while True:
        # 获取用户输入
        user_input = input("\n请输入您的问题: ").strip()
        
        if user_input.lower() == 'quit':
            print("感谢使用，再见！")
            break
            
        if not user_input:
            print("请输入有效的问题！")
            continue
            
        try:
            # 调用RAG链获取响应
            response = rag_chain.invoke(user_input)
            print(f"\nAI助手: {response}")
        except Exception as e:
            print(f"\n抱歉，处理您的问题时出现错误: {str(e)}")

if __name__ == "__main__":
    create_cli_interface() 