# 哈吉咪加密解密器 (Hachimi Crypto)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![C++](https://img.shields.io/badge/c%2B%2B-17%2B-blue.svg)

一个基于Python和C++联合编程的高性能加密解密工具，采用自定义的"哈吉咪"算法实现数据安全保护。

## 🌟 特性

- **高性能**：核心算法采用C++实现，确保最佳性能
- **易用性**：Python接口提供简洁的API调用
- **安全性**：实现多层加密算法，确保数据安全
- **跨平台**：支持Windows、Linux、macOS
- **灵活性**：支持文件和字符串两种加密模式

## 🚀 快速开始

### 环境要求

- Python 3.8+
- C++ 编译器 (支持C++17标准)
  - Windows: Visual Studio 2019+ 或 MinGW-w64
  - Linux: GCC 7+ 或 Clang 6+
  - macOS: Xcode 10+

### 安装

1. **克隆项目**
```bash
git clone https://github.com/jgbrzzh/Hachimi.git
cd Hachimi
```

2. **安装Python依赖**
```bash
pip install -r requirements.txt
```

3. **编译C++模块**
```bash
# Windows (使用Visual Studio)
python setup.py build_ext --inplace

# Linux/macOS
make build
```

### 基本使用

```python
from hachimi import HachimiCrypto

# 创建加密器实例
crypto = HachimiCrypto()

# 字符串加密/解密
plaintext = "Hello, 哈吉咪！"
encrypted = crypto.encrypt_string(plaintext, key="my_secret_key")
decrypted = crypto.decrypt_string(encrypted, key="my_secret_key")

print(f"原文: {plaintext}")
print(f"密文: {encrypted}")
print(f"解密: {decrypted}")

# 文件加密/解密
crypto.encrypt_file("input.txt", "output.encrypted", key="my_secret_key")
crypto.decrypt_file("output.encrypted", "decrypted.txt", key="my_secret_key")
```

## 📖 API 文档

### HachimiCrypto 类

#### 方法

- `encrypt_string(text: str, key: str) -> str`
  - 加密字符串
  - 参数：
    - `text`: 待加密的字符串
    - `key`: 加密密钥
  - 返回：加密后的Base64编码字符串

- `decrypt_string(encrypted_text: str, key: str) -> str`
  - 解密字符串
  - 参数：
    - `encrypted_text`: 加密的Base64编码字符串
    - `key`: 解密密钥
  - 返回：原始字符串

- `encrypt_file(input_path: str, output_path: str, key: str) -> bool`
  - 加密文件
  - 参数：
    - `input_path`: 输入文件路径
    - `output_path`: 输出文件路径
    - `key`: 加密密钥
  - 返回：操作是否成功

- `decrypt_file(input_path: str, output_path: str, key: str) -> bool`
  - 解密文件
  - 参数：
    - `input_path`: 加密文件路径
    - `output_path`: 输出文件路径
    - `key`: 解密密钥
  - 返回：操作是否成功

## 🏗️ 项目结构

```
Hachimi/
├── src/
│   ├── python/
│   │   ├── hachimi/
│   │   │   ├── __init__.py
│   │   │   ├── crypto.py          # Python接口
│   │   │   └── utils.py           # 工具函数
│   │   └── setup.py               # 构建脚本
│   └── cpp/
│       ├── include/
│       │   └── hachimi_core.h     # C++头文件
│       ├── src/
│       │   ├── hachimi_core.cpp   # 核心算法实现
│       │   └── python_binding.cpp # Python绑定
│       └── CMakeLists.txt         # CMake配置
├── tests/
│   ├── test_crypto.py             # 单元测试
│   └── benchmark.py               # 性能测试
├── examples/
│   ├── basic_usage.py             # 基本使用示例
│   ├── file_encryption.py         # 文件加密示例
│   └── batch_processing.py        # 批量处理示例
├── docs/
│   ├── algorithm.md               # 算法说明
│   ├── performance.md             # 性能分析
│   └── security.md                # 安全性说明
├── requirements.txt               # Python依赖
├── setup.py                       # 安装脚本
├── Makefile                       # 构建配置
├── README.md                      # 项目说明
└── LICENSE                        # 许可证
```

## 🔧 开发指南

### 构建开发环境

1. **安装开发依赖**
```bash
pip install -r requirements-dev.txt
```

2. **运行测试**
```bash
python -m pytest tests/ -v
```

3. **代码格式化**
```bash
black src/python/
clang-format -i src/cpp/src/*.cpp src/cpp/include/*.h
```

### 性能优化

- C++核心算法采用SIMD指令集优化
- 支持多线程并行处理大文件
- 内存池管理减少动态分配开销

## 🛡️ 安全说明

- 采用AES-256标准加密算法作为基础
- 实现了自定义的密钥派生函数(KDF)
- 支持随机盐值防止彩虹表攻击
- 密钥不会以明文形式存储在内存中

⚠️ **重要提示**: 请妥善保管您的加密密钥，密钥丢失将无法恢复加密数据。

## 📊 性能基准

| 操作类型 | 数据大小 | 处理时间 | 吞吐量 |
|---------|----------|----------|--------|
| 字符串加密 | 1KB | 0.1ms | 10MB/s |
| 字符串解密 | 1KB | 0.1ms | 10MB/s |
| 文件加密 | 100MB | 2.5s | 40MB/s |
| 文件解密 | 100MB | 2.3s | 43MB/s |

*测试环境: Intel i7-10700K, 32GB RAM, Windows 11*

## 🤝 贡献指南

1. Fork 项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 代码规范

- Python: 遵循 PEP 8 标准
- C++: 遵循 Google C++ Style Guide
- 提交信息: 使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式

## 📝 更新日志

### v1.0.0 (2025-09-21)
- ✨ 初始版本发布
- 🚀 实现基础加密解密功能
- 🔧 Python/C++混合编程架构
- 📚 完整的文档和示例

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 👨‍💻 作者

- **jgbrzzh** - 项目创建者和维护者

## 🙏 致谢

- 感谢所有为开源加密算法做出贡献的开发者
- 特别感谢 Python 和 C++ 社区的支持

## 📮 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 [Issue](https://github.com/jgbrzzh/Hachimi/issues)
- 发送邮件至项目维护者

---

<p align="center">
  <sub>Built with ❤️ and ☕ by the Hachimi team</sub>
</p>