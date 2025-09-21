"""
哈吉咪加密解密器

一个基于Python和C++联合编程的高性能加密解密工具。
"""

from .crypto import (
    HachimiCrypto,
    encrypt_string,
    decrypt_string, 
    encrypt_file,
    decrypt_file,
    __version__,
    __author__
)

__all__ = [
    'HachimiCrypto',
    'encrypt_string',
    'decrypt_string',
    'encrypt_file', 
    'decrypt_file',
    '__version__',
    '__author__'
]