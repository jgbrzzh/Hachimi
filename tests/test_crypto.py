#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈吉咪加密解密器单元测试

这个测试套件验证哈吉咪加密解密器的各种功能和边界条件。
"""

import os
import sys
import unittest
import tempfile
import shutil

# 添加src路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'python'))

try:
    from hachimi import HachimiCrypto, encrypt_string, decrypt_string, encrypt_file, decrypt_file
except ImportError:
    print("警告: 无法导入hachimi模块。请先运行 'python setup.py build_ext --inplace'")
    sys.exit(1)

class TestHachimiCrypto(unittest.TestCase):
    """HachimiCrypto类的测试用例"""
    
    def setUp(self):
        """测试前的设置"""
        self.crypto = HachimiCrypto()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """测试后的清理"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_basic_string_encryption_decryption(self):
        """测试基本字符串加密解密"""
        plaintext = "Hello, World!"
        key = "test_key"
        
        encrypted = self.crypto.encrypt_string(plaintext, key)
        self.assertIsInstance(encrypted, str)
        self.assertNotEqual(encrypted, plaintext)
        
        decrypted = self.crypto.decrypt_string(encrypted, key)
        self.assertEqual(decrypted, plaintext)
    
    def test_chinese_text_encryption(self):
        """测试中文文本加密"""
        plaintext = "哈吉咪加密解密器测试中文内容"
        key = "中文密钥"
        
        encrypted = self.crypto.encrypt_string(plaintext, key)
        decrypted = self.crypto.decrypt_string(encrypted, key)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_empty_string_handling(self):
        """测试空字符串处理"""
        with self.assertRaises(ValueError):
            self.crypto.encrypt_string("", "key")
        
        with self.assertRaises(ValueError):
            self.crypto.encrypt_string("text", "")
    
    def test_none_input_handling(self):
        """测试None输入处理"""
        with self.assertRaises(ValueError):
            self.crypto.encrypt_string(None, "key")
        
        with self.assertRaises(ValueError):
            self.crypto.encrypt_string("text", None)
    
    def test_wrong_key_decryption(self):
        """测试错误密钥解密"""
        plaintext = "Secret message"
        correct_key = "correct_key"
        wrong_key = "wrong_key"
        
        encrypted = self.crypto.encrypt_string(plaintext, correct_key)
        
        # 使用错误密钥解密应该得到不同的结果或抛出异常
        try:
            decrypted = self.crypto.decrypt_string(encrypted, wrong_key)
            self.assertNotEqual(decrypted, plaintext)
        except Exception:
            # 抛出异常也是可接受的行为
            pass
    
    def test_invalid_base64_decryption(self):
        """测试无效Base64解密"""
        with self.assertRaises((ValueError, RuntimeError)):
            self.crypto.decrypt_string("这不是有效的Base64", "key")
    
    def test_long_text_encryption(self):
        """测试长文本加密"""
        plaintext = "A" * 10000  # 10KB文本
        key = "long_text_key"
        
        encrypted = self.crypto.encrypt_string(plaintext, key)
        decrypted = self.crypto.decrypt_string(encrypted, key)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_special_characters(self):
        """测试特殊字符"""
        plaintext = "!@#$%^&*()_+-=[]{}|;':\",./<>?`~"
        key = "special_key"
        
        encrypted = self.crypto.encrypt_string(plaintext, key)
        decrypted = self.crypto.decrypt_string(encrypted, key)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_unicode_characters(self):
        """测试Unicode字符"""
        plaintext = "αβγδε ñáéíóú 你好世界 🔐🌟⭐"
        key = "unicode_key"
        
        encrypted = self.crypto.encrypt_string(plaintext, key)
        decrypted = self.crypto.decrypt_string(encrypted, key)
        
        self.assertEqual(decrypted, plaintext)

class TestFileOperations(unittest.TestCase):
    """文件操作的测试用例"""
    
    def setUp(self):
        """测试前的设置"""
        self.crypto = HachimiCrypto()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """测试后的清理"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_file_encryption_decryption(self):
        """测试文件加密解密"""
        # 创建测试文件
        input_file = os.path.join(self.temp_dir, "input.txt")
        encrypted_file = os.path.join(self.temp_dir, "encrypted.dat")
        decrypted_file = os.path.join(self.temp_dir, "decrypted.txt")
        
        test_content = "这是一个测试文件\nWith multiple lines\n包含中英文内容"
        
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        key = "file_test_key"
        
        # 加密文件
        success = self.crypto.encrypt_file(input_file, encrypted_file, key)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(encrypted_file))
        
        # 解密文件
        success = self.crypto.decrypt_file(encrypted_file, decrypted_file, key)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(decrypted_file))
        
        # 验证内容
        with open(decrypted_file, 'r', encoding='utf-8') as f:
            decrypted_content = f.read()
        
        self.assertEqual(decrypted_content, test_content)
    
    def test_binary_file_encryption(self):
        """测试二进制文件加密"""
        input_file = os.path.join(self.temp_dir, "binary.dat")
        encrypted_file = os.path.join(self.temp_dir, "binary_encrypted.dat")
        decrypted_file = os.path.join(self.temp_dir, "binary_decrypted.dat")
        
        # 创建二进制测试数据
        test_data = bytes(range(256)) * 10  # 2560 bytes
        
        with open(input_file, 'wb') as f:
            f.write(test_data)
        
        key = "binary_test_key"
        
        # 加密文件
        success = self.crypto.encrypt_file(input_file, encrypted_file, key)
        self.assertTrue(success)
        
        # 解密文件
        success = self.crypto.decrypt_file(encrypted_file, decrypted_file, key)
        self.assertTrue(success)
        
        # 验证内容
        with open(decrypted_file, 'rb') as f:
            decrypted_data = f.read()
        
        self.assertEqual(decrypted_data, test_data)
    
    def test_nonexistent_file(self):
        """测试不存在的文件"""
        nonexistent_file = os.path.join(self.temp_dir, "nonexistent.txt")
        output_file = os.path.join(self.temp_dir, "output.dat")
        
        with self.assertRaises(FileNotFoundError):
            self.crypto.encrypt_file(nonexistent_file, output_file, "key")
    
    def test_empty_file(self):
        """测试空文件"""
        empty_file = os.path.join(self.temp_dir, "empty.txt")
        encrypted_file = os.path.join(self.temp_dir, "empty_encrypted.dat")
        
        # 创建空文件
        with open(empty_file, 'w') as f:
            pass
        
        # 空文件加密应该失败或返回False
        success = self.crypto.encrypt_file(empty_file, encrypted_file, "key")
        self.assertFalse(success)

class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数的测试用例"""
    
    def test_module_level_functions(self):
        """测试模块级别的便捷函数"""
        plaintext = "测试便捷函数"
        key = "convenience_key"
        
        encrypted = encrypt_string(plaintext, key)
        decrypted = decrypt_string(encrypted, key)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_file_convenience_functions(self):
        """测试文件便捷函数"""
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = os.path.join(temp_dir, "input.txt")
            encrypted_file = os.path.join(temp_dir, "encrypted.dat")
            decrypted_file = os.path.join(temp_dir, "decrypted.txt")
            
            test_content = "便捷函数文件测试"
            
            with open(input_file, 'w', encoding='utf-8') as f:
                f.write(test_content)
            
            key = "file_convenience_key"
            
            # 使用便捷函数
            success1 = encrypt_file(input_file, encrypted_file, key)
            success2 = decrypt_file(encrypted_file, decrypted_file, key)
            
            self.assertTrue(success1)
            self.assertTrue(success2)
            
            with open(decrypted_file, 'r', encoding='utf-8') as f:
                decrypted_content = f.read()
            
            self.assertEqual(decrypted_content, test_content)

class TestModuleAttributes(unittest.TestCase):
    """模块属性测试"""
    
    def test_version_and_connection(self):
        """测试版本信息和连接"""
        crypto = HachimiCrypto()
        
        # 测试版本信息
        version = crypto.get_version()
        self.assertIsInstance(version, str)
        self.assertIn("1.0.0", version)
        
        # 测试连接
        connection = crypto.test_connection()
        self.assertIsInstance(connection, str)
        self.assertIn("working", connection.lower())

def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    test_classes = [
        TestHachimiCrypto,
        TestFileOperations,
        TestConvenienceFunctions,
        TestModuleAttributes
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    print("🧪 哈吉咪加密解密器 - 单元测试")
    print("=" * 50)
    
    success = run_tests()
    
    if success:
        print("\n✓ 所有测试通过!")
        sys.exit(0)
    else:
        print("\n✗ 部分测试失败!")
        sys.exit(1)