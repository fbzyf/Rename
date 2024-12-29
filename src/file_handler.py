from typing import Final, Union
import os
import re
from pathlib import Path
import logging
from datetime import datetime

class FileHandler:
    """处理文件重命名的类"""
    
    # 文件名相关常量
    INVALID_CHARS: Final[str] = r'[\\/:*?"<>|]'
    MAX_FILENAME_LENGTH: Final[int] = 255  # Windows 最大文件名长度
    
    def __init__(self, log_dir: str = "logs") -> None:
        """
        初始化文件处理器
        
        Args:
            log_dir: 日志文件目录
        """
        self.log_dir = Path(log_dir)
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """设置日志记录"""
        self.log_dir.mkdir(exist_ok=True)
        log_file = self.log_dir / f"rename_{datetime.now():%Y%m%d}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
    
    def sanitize_filename(self, filename: str) -> str:
        """
        清理文件名中的非法字符
        
        Args:
            filename: 原始文件名
            
        Returns:
            清理后的文件名
        """
        # 替换非法字符
        clean_name = re.sub(self.INVALID_CHARS, '', filename)
        # 移除前后空白
        clean_name = clean_name.strip()
        # 确保文件名不为空
        if not clean_name:
            clean_name = f"unnamed_{datetime.now():%Y%m%d_%H%M%S}"
        # 限制长度
        return clean_name[:self.MAX_FILENAME_LENGTH]
    
    def _normalize_path(self, path: Union[str, Path]) -> Path:
        """
        规范化文件路径
        
        Args:
            path: 文件路径
            
        Returns:
            规范化后的路径
        """
        # 转换为 Path 对象
        path = Path(path)
        
        try:
            # 转换为绝对路径并规范化
            return path.resolve()
        except Exception as e:
            logging.error(f"路径规范化失败: {path}, 错误: {e}")
            return path
    
    def rename_file(self, old_path: Union[str, Path], new_name: str) -> str:
        """
        重命名文件
        
        Args:
            old_path: 原文件路径
            new_name: 新文件名（不含扩展名）
            
        Returns:
            新的文件路径
            
        Raises:
            FileNotFoundError: 原文件不存在
            PermissionError: 没有权限重命名文件
            Exception: 其他错误
        """
        try:
            old_path = self._normalize_path(old_path)
            if not old_path.exists():
                raise FileNotFoundError(f"文件不存在: {old_path}")
            
            # 获取文件目录和扩展名
            directory = old_path.parent
            extension = old_path.suffix
            
            # 清理新文件名
            clean_name = self.sanitize_filename(new_name)
            
            # 构建新的文件路径
            new_path = directory / f"{clean_name}{extension}"
            
            # 如果文件已存在，添加序号
            counter = 1
            while new_path.exists():
                new_path = directory / f"{clean_name}_{counter}{extension}"
                counter += 1
            
            # 重命名文件
            old_path.rename(new_path)
            
            # 记录日志
            logging.info(f"重命名文件: {old_path} -> {new_path}")
            
            return str(new_path)
            
        except FileNotFoundError:
            logging.error(f"文件不存在: {old_path}")
            raise
        except PermissionError:
            logging.error(f"没有权限重命名文件: {old_path}")
            raise
        except Exception as e:
            logging.error(f"重命名文件失败: {str(e)}")
            raise Exception(f"重命名文件失败: {str(e)}") 