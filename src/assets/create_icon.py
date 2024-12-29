from PIL import Image, ImageDraw
import os

def create_icon():
    # 创建 64x64 的图标
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制简单的图标设计
    draw.rectangle([8, 8, 56, 56], outline=(0, 120, 212), width=2)
    draw.rectangle([16, 16, 48, 48], fill=(0, 120, 212))
    
    # 保存为 ICO 文件
    img.save('src/assets/icon.ico', format='ICO')

if __name__ == '__main__':
    create_icon() 