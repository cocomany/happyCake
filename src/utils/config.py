"""
配置管理模块
作者: 越山
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict

# 加载环境变量
load_dotenv()

class Config(BaseModel):
    """系统配置类"""
    
    # 禁用受保护的命名空间检查
    model_config = ConfigDict(protected_namespaces=())
   
    # API配置
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_api_base: str = os.getenv("OPENAI_API_BASE", "https://api.deepseek.com/v1")
    model_name: str = os.getenv("OPENAI_MODEL_NAME", "deepseek-chat")
    dashscope_api_key: str = os.getenv("DASHSCOPE_API_KEY", "")
    
    # 向量存储配置
    vector_store_path: Path = Path(os.getenv("VECTOR_STORE_PATH", "./vector_store"))
    
    # 知识库路径
    knowledge_base_path: Path = Path("knowledge_base")
    
    # 日志配置
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    def validate_config(self) -> bool:
        """验证配置是否完整"""
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not found in environment variables")
            
        if not self.dashscope_api_key:
            raise ValueError("DashScope API key not found in environment variables")
        
        if not self.knowledge_base_path.exists():
            raise ValueError(f"Knowledge base directory not found at {self.knowledge_base_path}")
        
        return True

# 创建全局配置实例
config = Config()

# 验证配置
config.validate_config() 