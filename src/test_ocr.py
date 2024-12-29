import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
sys.path.append(str(Path(__file__).parent.parent))

from src.ocr_handler import OCRHandler
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_ocr():
    # 创建 OCR 处理器
    try:
        ocr = OCRHandler()
        logging.info("OCR 初始化成功")
    except Exception as e:
        logging.error(f"OCR 初始化失败: {e}")
        return False
    
    # 测试图片目录
    test_dir = Path("tests/images")
    
    # 测试不同类型的图片
    test_files = {
        "中文测试": test_dir / "test_cn.png",
        "英文测试": test_dir / "test_en.png",
        "混合测试": test_dir / "test_mixed.png",
        "空白测试": test_dir / "test_empty.png"
    }
    
    success = True
    for test_name, test_file in test_files.items():
        try:
            logging.info(f"\n开始{test_name}...")
            if not test_file.exists():
                logging.warning(f"测试文件不存在: {test_file}")
                continue
                
            # 测试文字识别
            text = ocr.extract_text(test_file)
            logging.info(f"识别结果: {text}")
            
        except Exception as e:
            logging.error(f"{test_name}失败: {e}")
            success = False
    
    return success

if __name__ == "__main__":
    success = test_ocr()
    if success:
        logging.info("所有测试完成")
    else:
        logging.error("测试过程中出现错误") 