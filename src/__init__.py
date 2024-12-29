"""
Screenshot Renamer
一个智能截图重命名工具 - 使用 AI 自动提取文本并生成规范的文件名
"""

__version__ = "1.0.0"

from .ocr_handler import OCRHandler
from .ai_handler import AIHandler
from .file_handler import FileHandler
from .config import Config

__all__ = ['OCRHandler', 'AIHandler', 'FileHandler', 'Config'] 