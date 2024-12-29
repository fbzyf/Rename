import easyocr
from typing import Final
from typing import Union, List, Tuple, Any
from pathlib import Path
import numpy as np
import numpy.typing as npt
from PIL import Image
import cv2
import logging
import os

class OCRHandler:
    """处理 OCR 文字识别的类"""
    
    def __init__(self) -> None:
        """初始化 OCR 处理器"""
        try:
            # 初始化 EasyOCR，支持中文和英文
            self.reader = easyocr.Reader(['ch_sim', 'en'])
        except Exception as e:
            raise RuntimeError(f"OCR 初始化失败: {str(e)}")
    
    def _validate_image(self, image_path: Union[str, Path]) -> bool:
        """
        验证图片是否可用
        
        Args:
            image_path: 图片路径
            
        Returns:
            bool: 图片是否有效
        """
        try:
            # 尝试用 PIL 打开图片
            with Image.open(str(image_path)) as img:
                img.verify()
            return True
        except Exception as e:
            logging.warning(f"图片验证失败: {image_path}, 错误: {e}")
            return False
    
    def extract_text(self, image_path: Union[str, Path, npt.NDArray[Any]]) -> str:
        """
        识别图片中的文字
        
        Args:
            image_path: 图片文件路径或图像数组
            
        Returns:
            识别出的文字内容
            
        Raises:
            Exception: OCR 处理失败时抛出异常
        """
        try:
            # 如果是路径，先验证图片
            if isinstance(image_path, (str, Path)):
                if not self._validate_image(image_path):
                    raise ValueError(f"无效的图片文件: {image_path}")
                
                # 使用 PIL 读取图片（更好地处理中文路径）
                try:
                    with Image.open(str(image_path)) as img:
                        # 转换为 RGB 模式
                        if img.mode != 'RGB':
                            img = img.convert('RGB')
                        # 转换为 numpy 数组
                        image = np.array(img)
                except Exception as e:
                    raise ValueError(f"无法读取图片: {image_path}, 错误: {str(e)}")
            else:
                image = image_path
            
            # 执行文字识别
            result = self.reader.readtext(image)
            
            if not result:
                return ""
            
            # 提取所有识别出的文字
            texts: List[str] = []
            for detection in result:
                text = detection[1]  # 文字内容
                confidence = detection[2]  # 置信度
                
                # 只添加置信度大于 0.5 的非空文本
                if text.strip() and confidence > 0.5:
                    texts.append(text)
            
            # 合并所有文字
            return " ".join(texts)
            
        except ValueError as e:
            # 重新抛出验证错误
            raise
        except Exception as e:
            raise Exception(f"OCR 处理失败: {str(e)}") 