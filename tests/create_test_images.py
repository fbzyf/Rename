from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_test_image(text: str, filename: str) -> None:
    """创建测试图片"""
    # 创建空白图片
    img = Image.new('RGB', (400, 100), color='white')
    d = ImageDraw.Draw(img)
    
    # 使用系统字体
    try:
        font = ImageFont.truetype("msyh.ttc", 24)  # 微软雅黑
    except:
        font = ImageFont.load_default()
    
    # 绘制文字
    d.text((10, 10), text, font=font, fill='black')
    
    # 保存图片
    img_path = Path("tests/images") / filename
    img_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(img_path)

if __name__ == "__main__":
    # 创建测试图片
    create_test_image("这是一个中文测试", "test_cn.png")
    create_test_image("This is an English test", "test_en.png")
    create_test_image("中英混合 Mixed Text 测试", "test_mixed.png")
    create_test_image("", "test_empty.png") 