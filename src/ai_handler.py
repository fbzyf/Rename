from typing import Final
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

class AIHandler:
    """处理 AI 文本总结的类"""
    
    # API 配置常量
    API_URL: Final[str] = "https://api.deepseek.com/v1/chat/completions"
    MAX_FILENAME_LENGTH: Final[int] = 50  # 增加长度以容纳更多信息
    MAX_RETRIES: Final[int] = 3
    
    def __init__(self, api_key: str) -> None:
        """
        初始化 AI 处理器
        
        Args:
            api_key: DeepSeek API 密钥
        """
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    @retry(
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def generate_filename(self, text: str) -> str:
        """
        使用 DeepSeek API 生成文件名
        
        Args:
            text: 需要总结的文本内容
            
        Returns:
            生成的文件名
            
        Raises:
            Exception: API 调用失败时抛出异常
        """
        try:
            prompt = (
                "你是一个专业的文件命名专家，需要将截图中的文字内容转换为一个清晰、规范的文件名。\n\n"
                "命名规则：\n"
                "1. 结构：[主题]_[类型]_[日期]\n"
                "2. 主题：提取最核心的2-3个关键词，优先选择名词性词组\n"
                "3. 类型：如文档/报告/笔记/截图等\n"
                "4. 日期：仅当文本内容中明确包含日期时才添加日期，格式为YYYYMMDD\n"
                "   - 如果文本中没有日期，则不要在文件名中添加日期\n"
                "   - 不要自动添加当前日期\n"
                "5. 语言：优先使用中文，英文内容可保留英文\n"
                "6. 分隔：使用下划线连接不同部分\n"
                "7. 长度：总长度不超过50个字符\n"
                "8. 禁止：特殊字符、空格、重复信息\n"
                "9. 注意：\n"
                "   - 界面截图应标记为'界面'类型\n"
                "   - 代码截图应标记为'代码'类型\n"
                "   - 文档截图应标记为'文档'类型\n\n"
                f"文本内容：{text}\n\n"
                "请直接返回文件名，不需要解释。示例：\n"
                "- 有日期的例子：产品需求_文档_20231229\n"
                "- 无日期的例子：登录界面_界面"
            )
            
            data = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,  # 降低随机性
                "max_tokens": 30     # 限制输出长度以获得更简洁的结果
            }
            
            response = requests.post(
                self.API_URL,
                headers=self.headers,
                json=data,
                timeout=10  # 10秒超时
            )
            
            response.raise_for_status()  # 检查响应状态
            
            filename = response.json()["choices"][0]["message"]["content"].strip()
            logging.info(f"AI 生成文件名: {filename}")
            
            # 确保不超过长度限制
            return filename[:self.MAX_FILENAME_LENGTH]
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API 请求失败: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"API 响应格式错误: {str(e)}")
        except Exception as e:
            raise Exception(f"生成文件名失败: {str(e)}") 