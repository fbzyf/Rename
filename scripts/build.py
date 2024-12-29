"""打包脚本"""
import os
import shutil
from pathlib import Path

def clean_build():
    """清理构建文件"""
    dirs_to_clean = ['build', 'dist', 'temp']
    files_to_clean = []
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    for pattern in files_to_clean:
        for file in Path('.').glob(pattern):
            file.unlink()

def build():
    """构建可执行文件"""
    # 清理旧的构建文件
    clean_build()
    
    # 创建资源目录
    os.makedirs('build/resources', exist_ok=True)
    
    # 复制必要的资源文件
    shutil.copy('README.md', 'build/resources/')
    
    # 使用 PyInstaller 打包
    os.system('pyinstaller main.spec --clean --workpath build/temp --distpath release')
    
    print("构建完成！可执行文件位于 release 目录")

if __name__ == '__main__':
    build() 