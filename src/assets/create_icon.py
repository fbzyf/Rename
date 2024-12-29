from PIL import Image, ImageDraw

# 创建一个 256x256 的图像
size = 256
img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# 绘制一个简单的图标
margin = size // 8
draw.rectangle(
    [margin, margin, size-margin, size-margin],
    fill=(52, 53, 65, 255),
    outline=(82, 83, 95, 255),
    width=4
)

# 绘制一个文档符号
doc_margin = size // 4
draw.rectangle(
    [doc_margin, doc_margin, size-doc_margin, size-doc_margin],
    fill=(255, 255, 255, 255),
    outline=(82, 83, 95, 255),
    width=2
)

# 绘制文本线条
line_margin = size // 3
line_height = size // 16
for i in range(3):
    y = line_margin + i * (line_height * 2)
    draw.line(
        [line_margin, y, size-line_margin, y],
        fill=(82, 83, 95, 255),
        width=2
    )

# 保存为 ICO 文件
img.save('icon.ico', format='ICO') 