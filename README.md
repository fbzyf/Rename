# Screenshot Auto Renamer v1.0.0

一个智能截图重命名工具，可以自动识别截图中的文字内容，并生成规范的文件名。

## 主要特性

### 文字识别
- 支持中文（简体/繁体）和英文
- 使用 EasyOCR 引擎，准确率高
- 自动处理图片方向和格式

### AI 智能命名
- 使用 DeepSeek AI 提取核心内容
- 智能分析文本结构和类型
- 自动识别和保留日期信息
- 生成规范的文件名格式：[主题]_[类型]_[日期]

### 批量处理
- 支持单个或多个文件选择
- 支持文件夹递归处理
- 自动跳过无效文件
- 实时显示处理进度

### 用户界面
- 简洁直观的操作界面
- 深色主题支持
- 实时状态反馈
- 详细的处理结果展示

## 使用方法

1. 运行程序
2. 选择文件或文件夹：
   - 点击"选择文件"按钮选择单个或多个截图
   - 点击"选择文件夹"按钮选择包含截图的文件夹
3. 程序会自动开始处理
4. 处理完成后可以查看结果

## 安装说明

### 方法一：直接运行
1. 下载发布包中的 ScreenshotRenamer.exe
2. 双击运行即可使用

### 方法二：从源码安装
```bash
# 克隆仓库
git clone https://github.com/yourusername/Rename.git
cd Rename

# 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行程序
python src/main.py
```

## 系统要求

- Windows 7 及以上系统
- Python 3.10 或更高版本
- 2GB 以上可用内存

## 技术栈

- Python 3.12
- EasyOCR：文字识别引擎
- DeepSeek：AI 文本处理
- CustomTkinter：用户界面
- PyInstaller：程序打包

## 更新日志

### v1.0.0 (2023-12-29)
- 首个稳定版本发布
- 完整的文件处理功能
- 智能文件名生成
- 批量处理支持
- 实时进度显示

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件 