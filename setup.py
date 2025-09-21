"""
哈吉咪加密解密器安装脚本

这个脚本使用pybind11编译C++扩展模块并安装Python包。
"""

import os
import sys
from pathlib import Path
from pybind11.setup_helpers import Pybind11Extension, build_ext, Pybind11CMakeHelper
from setuptools import setup, find_packages

# 项目信息
NAME = "hachimi"
VERSION = "1.0.0"
DESCRIPTION = "高性能哈吉咪加密解密器"
LONG_DESCRIPTION = """
哈吉咪加密解密器是一个基于Python和C++联合编程的高性能加密解密工具。

特性:
- 高性能: 核心算法采用C++实现
- 易用性: Python接口提供简洁的API
- 安全性: 实现多层加密算法
- 跨平台: 支持Windows、Linux、macOS

使用方法:
    from hachimi import HachimiCrypto
    
    crypto = HachimiCrypto()
    encrypted = crypto.encrypt_string("Hello, World!", "my_key")
    decrypted = crypto.decrypt_string(encrypted, "my_key")
"""

# 获取项目根目录
ROOT_DIR = Path(__file__).parent.absolute()
SRC_DIR = ROOT_DIR / "src"
CPP_DIR = SRC_DIR / "cpp"
PYTHON_DIR = SRC_DIR / "python"

# C++源文件
cpp_sources = [
    str(CPP_DIR / "src" / "hachimi_core.cpp"),
    str(CPP_DIR / "src" / "python_binding.cpp")
]

# 包含目录
include_dirs = [
    str(CPP_DIR / "include")
]

# 编译器参数
cpp_std = 17
compile_args = []
link_args = []

if sys.platform == "win32":
    # Windows 特定设置
    compile_args.extend([
        "/std:c++17",
        "/O2",           # 优化
        "/MD",           # 多线程DLL运行时库
        "/EHsc",         # 异常处理
    ])
elif sys.platform.startswith("linux"):
    # Linux 特定设置
    compile_args.extend([
        "-std=c++17",
        "-O3",           # 最高优化
        "-fPIC",         # 位置无关代码
        "-march=native", # 本机优化
    ])
elif sys.platform == "darwin":
    # macOS 特定设置
    compile_args.extend([
        "-std=c++17",
        "-O3",
        "-fPIC",
        "-march=native",
        "-mmacosx-version-min=10.14",  # 最低macOS版本
    ])

# 定义扩展模块
ext_modules = [
    Pybind11Extension(
        name="hachimi.hachimi_core",
        sources=cpp_sources,
        include_dirs=include_dirs,
        cxx_std=cpp_std,
        extra_compile_args=compile_args,
        extra_link_args=link_args,
        language="c++"
    )
]

# 自定义构建类
class CustomBuildExt(build_ext):
    """自定义构建扩展类，添加额外的构建逻辑"""
    
    def build_extensions(self):
        # 检查编译器
        if self.compiler.compiler_type == "msvc":
            # Visual Studio 编译器特定设置
            for ext in self.extensions:
                ext.extra_compile_args.append("/bigobj")  # 处理大对象文件
        
        # 调用父类构建方法
        super().build_extensions()

# 读取依赖文件
def read_requirements():
    """读取requirements.txt文件"""
    requirements_file = ROOT_DIR / "requirements.txt"
    if requirements_file.exists():
        with open(requirements_file, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

# 设置安装配置
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/plain",
    author="jgbrzzh",
    author_email="",
    url="https://github.com/jgbrzzh/Hachimi",
    
    # 包设置
    package_dir={"": str(PYTHON_DIR)},
    packages=find_packages(where=str(PYTHON_DIR)),
    
    # C++扩展
    ext_modules=ext_modules,
    cmdclass={"build_ext": CustomBuildExt},
    
    # 依赖
    install_requires=read_requirements(),
    python_requires=">=3.8",
    
    # 分类信息
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: C++",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
    ],
    
    # 关键词
    keywords="encryption, decryption, cryptography, security, performance",
    
    # 项目URL
    project_urls={
        "Bug Reports": "https://github.com/jgbrzzh/Hachimi/issues",
        "Source": "https://github.com/jgbrzzh/Hachimi",
        "Documentation": "https://github.com/jgbrzzh/Hachimi/blob/master/README.md",
    },
    
    # 包含的数据文件
    include_package_data=True,
    
    # zip_safe设为False，因为包含C++扩展
    zip_safe=False,
)