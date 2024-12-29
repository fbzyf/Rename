"""创建 spec 文件"""
from pathlib import Path

def create_spec():
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('README.md', '.'),
        ('src/assets/icon.ico', 'assets'),
        ('config.json', '.'),
    ],
    hiddenimports=[
        'customtkinter',
        'easyocr',
        'torch',
        'torchvision',
        'numpy',
        'PIL',
        'cv2',
        'src',
        'src.config',
        'src.ocr_handler',
        'src.ai_handler',
        'src.file_handler',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ScreenshotRenamer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='src/assets/icon.ico',
    version='file_version_info.txt'
)
'''
    
    with open('main.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print("main.spec 文件已创建")

if __name__ == '__main__':
    create_spec() 