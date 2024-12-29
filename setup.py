from setuptools import setup, find_packages
from typing import Dict, List

setup(
    name="screenshot_renamer",
    version="1.0.0",
    packages=find_packages(),
    package_data={
        "screenshot_renamer": ["py.typed"],
    },
    install_requires: List[str] = [
        "Pillow>=10.0.0",
        "easyocr>=1.7.0",
        "customtkinter>=5.2.0",
        "requests>=2.31.0",
        "tenacity>=8.2.0",
    ],
    python_requires=">=3.10",
) 