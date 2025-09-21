"""
哈吉咪加密解密器 - Python接口

这个模块提供了一个简单而强大的加密解密接口，
底层使用C++实现以确保高性能。
"""

import base64
import os
from typing import Union, Optional

try:
    # 导入C++扩展模块
    from . import hachimi_core as _core
except ImportError:
    try:
        # 如果作为独立模块运行，尝试直接导入
        import hachimi_core as _core
    except ImportError:
        raise ImportError(
            "无法导入C++扩展模块。请确保已正确编译和安装hachimi_core模块。"
        )

__version__ = "1.0.0"
__author__ = "jgbrzzh"

class HachimiCrypto:
    """
    哈吉咪加密解密器主类
    
    这个类提供了简单易用的加密解密接口，支持字符串和文件的加密解密。
    底层使用高性能的C++实现。
    
    Examples:
        >>> crypto = HachimiCrypto()
        >>> encrypted = crypto.encrypt_string("Hello, 哈吉咪！", "my_key")
        >>> decrypted = crypto.decrypt_string(encrypted, "my_key")
        >>> print(decrypted)
        Hello, 哈吉咪！
    """
    
    def __init__(self):
        """初始化哈吉咪加密器"""
        self._core = _core.HachimiCore()
    
    def encrypt_string(self, plaintext: str, key: str) -> str:
        """
        加密字符串
        
        Args:
            plaintext: 待加密的字符串
            key: 加密密钥
            
        Returns:
            Base64编码的加密字符串
            
        Raises:
            ValueError: 当输入参数无效时
            RuntimeError: 当加密失败时
        """
        if not isinstance(plaintext, str):
            raise ValueError("plaintext必须是字符串")
        if not isinstance(key, str):
            raise ValueError("key必须是字符串")
        if not plaintext:
            raise ValueError("plaintext不能为空")
        if not key:
            raise ValueError("key不能为空")
            
        try:
            # 调用C++核心加密函数
            encrypted_bytes = self._core.encrypt(plaintext, key)
            if not encrypted_bytes:
                raise RuntimeError("加密失败：C++模块返回空结果")
                
            # 转换为Base64编码
            return base64.b64encode(bytes(encrypted_bytes)).decode('utf-8')
        except Exception as e:
            raise RuntimeError(f"加密过程中发生错误: {str(e)}")
    
    def decrypt_string(self, encrypted_text: str, key: str) -> str:
        """
        解密字符串
        
        Args:
            encrypted_text: Base64编码的加密字符串
            key: 解密密钥
            
        Returns:
            解密后的原始字符串
            
        Raises:
            ValueError: 当输入参数无效时
            RuntimeError: 当解密失败时
        """
        if not isinstance(encrypted_text, str):
            raise ValueError("encrypted_text必须是字符串")
        if not isinstance(key, str):
            raise ValueError("key必须是字符串")
        if not encrypted_text:
            raise ValueError("encrypted_text不能为空")
        if not key:
            raise ValueError("key不能为空")
            
        try:
            # 从Base64解码
            encrypted_bytes = list(base64.b64decode(encrypted_text.encode('utf-8')))
            
            # 调用C++核心解密函数
            decrypted_text = self._core.decrypt(encrypted_bytes, key)
            if decrypted_text is None:
                raise RuntimeError("解密失败：可能是密钥错误或数据损坏")
                
            return decrypted_text
        except base64.binascii.Error:
            raise ValueError("encrypted_text不是有效的Base64编码")
        except Exception as e:
            raise RuntimeError(f"解密过程中发生错误: {str(e)}")
    
    def encrypt_file(self, input_path: str, output_path: str, key: str) -> bool:
        """
        加密文件
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            key: 加密密钥
            
        Returns:
            True如果加密成功，False否则
            
        Raises:
            ValueError: 当输入参数无效时
            FileNotFoundError: 当输入文件不存在时
            PermissionError: 当没有文件权限时
        """
        if not isinstance(input_path, str) or not input_path:
            raise ValueError("input_path必须是非空字符串")
        if not isinstance(output_path, str) or not output_path:
            raise ValueError("output_path必须是非空字符串")
        if not isinstance(key, str) or not key:
            raise ValueError("key必须是非空字符串")
            
        # 检查输入文件是否存在
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"输入文件不存在: {input_path}")
            
        # 检查输入文件是否可读
        if not os.access(input_path, os.R_OK):
            raise PermissionError(f"无法读取输入文件: {input_path}")
            
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except OSError as e:
                raise PermissionError(f"无法创建输出目录: {str(e)}")
        
        try:
            # 调用C++核心文件加密函数
            return self._core.encrypt_file(input_path, output_path, key)
        except Exception as e:
            raise RuntimeError(f"文件加密过程中发生错误: {str(e)}")
    
    def decrypt_file(self, input_path: str, output_path: str, key: str) -> bool:
        """
        解密文件
        
        Args:
            input_path: 加密文件路径
            output_path: 输出文件路径
            key: 解密密钥
            
        Returns:
            True如果解密成功，False否则
            
        Raises:
            ValueError: 当输入参数无效时
            FileNotFoundError: 当输入文件不存在时
            PermissionError: 当没有文件权限时
        """
        if not isinstance(input_path, str) or not input_path:
            raise ValueError("input_path必须是非空字符串")
        if not isinstance(output_path, str) or not output_path:
            raise ValueError("output_path必须是非空字符串")
        if not isinstance(key, str) or not key:
            raise ValueError("key必须是非空字符串")
            
        # 检查输入文件是否存在
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"输入文件不存在: {input_path}")
            
        # 检查输入文件是否可读
        if not os.access(input_path, os.R_OK):
            raise PermissionError(f"无法读取输入文件: {input_path}")
            
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except OSError as e:
                raise PermissionError(f"无法创建输出目录: {str(e)}")
        
        try:
            # 调用C++核心文件解密函数
            return self._core.decrypt_file(input_path, output_path, key)
        except Exception as e:
            raise RuntimeError(f"文件解密过程中发生错误: {str(e)}")
    
    def test_connection(self) -> str:
        """
        测试C++模块连接
        
        Returns:
            测试消息字符串
        """
        try:
            return _core.test_connection()
        except Exception as e:
            return f"连接测试失败: {str(e)}"
    
    def get_version(self) -> str:
        """
        获取版本信息
        
        Returns:
            版本字符串
        """
        try:
            core_version = _core.version()
            return f"Python包装器: {__version__}, C++核心: {core_version}"
        except Exception:
            return f"Python包装器: {__version__}, C++核心: 未知"

# 便捷函数
def encrypt_string(plaintext: str, key: str) -> str:
    """便捷的字符串加密函数"""
    crypto = HachimiCrypto()
    return crypto.encrypt_string(plaintext, key)

def decrypt_string(encrypted_text: str, key: str) -> str:
    """便捷的字符串解密函数"""
    crypto = HachimiCrypto()
    return crypto.decrypt_string(encrypted_text, key)

def encrypt_file(input_path: str, output_path: str, key: str) -> bool:
    """便捷的文件加密函数"""
    crypto = HachimiCrypto()
    return crypto.encrypt_file(input_path, output_path, key)

def decrypt_file(input_path: str, output_path: str, key: str) -> bool:
    """便捷的文件解密函数"""
    crypto = HachimiCrypto()
    return crypto.decrypt_file(input_path, output_path, key)