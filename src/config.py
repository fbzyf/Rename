"""配置文件模块"""
from pathlib import Path
from typing import Dict, Any
import json
import logging

DEFAULT_CONFIG = {
    "theme": "dark",
    "language": "zh_CN",
    "min_confidence": 0.5,
    "max_filename_length": 20,
    "supported_formats": [".png", ".jpg", ".jpeg", ".bmp"],
    "api_key": "sk-fdebc76759574fdc849ed0fd2cf79480"
}

class Config:
    """配置管理类"""
    
    def __init__(self) -> None:
        self.config_file = Path("config.json")
        self.config: Dict[str, Any] = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return DEFAULT_CONFIG.copy()
        except Exception as e:
            logging.error(f"加载配置文件失败: {e}")
            return DEFAULT_CONFIG.copy()
    
    def save(self) -> None:
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logging.error(f"保存配置文件失败: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """设置配置项"""
        self.config[key] = value
        self.save() 