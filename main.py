"""
项目入口文件
作者: 越山
"""
import argparse

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="甜品日记AI客服系统")
    parser.add_argument(
        "--mode",
        type=str,
        choices=["cli", "web"],
        default="cli",
        help="运行模式：cli(命令行界面) 或 web(网页界面)"
    )
    
    args = parser.parse_args()
    
    if args.mode == "cli":
        from src.cli.chat_cli import main as cli_main
        cli_main()
    else:
        try:
            from src.web.app import main as web_main
            web_main()
        except ImportError:
            print("Error: Gradio is not installed. To use web mode, please install it first:")
            print("pip install gradio>=4.14.0")
            exit(1)

if __name__ == "__main__":
    main() 