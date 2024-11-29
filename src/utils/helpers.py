"""
通用工具函数
作者: 越山
"""
import logging
from pathlib import Path
from typing import List

from .config import config

# 配置日志
logging.basicConfig(
    level=config.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_all_markdown_files(directory: Path) -> List[Path]:
    """获取指定目录下的所有Markdown文件"""
    if not directory.exists():
        logger.warning(f"Directory {directory} does not exist")
        return []
    
    return list(directory.glob("**/*.md"))

def read_markdown_file(file_path: Path) -> str:
    """读取Markdown文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return "" 