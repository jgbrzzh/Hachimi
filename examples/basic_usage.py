#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈吉咪加密解密器基本使用示例

这个示例展示了如何使用哈吉咪加密解密器进行基本的字符串和文件加密解密操作。
"""

import sys
import os

# 添加src路径以便导入hachimi模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'python'))

try:
    from hachimi import HachimiCrypto
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保已正确安装hachimi模块。")
    print("运行 'python setup.py build_ext --inplace' 来构建模块。")
    sys.exit(1)

def main():
    """主函数，演示基本使用方法"""
    print("🔐 哈吉咪加密解密器 - 基本使用示例")
    print("=" * 50)
    
    # 创建加密器实例
    try:
        crypto = HachimiCrypto()
        print("✓ 成功创建HachimiCrypto实例")
    except Exception as e:
        print(f"✗ 创建实例失败: {e}")
        return
    
    # 测试连接
    print("\n1. 测试C++模块连接")
    connection_result = crypto.test_connection()
    print(f"   连接测试结果: {connection_result}")
    
    # 获取版本信息
    version_info = crypto.get_version()
    print(f"   版本信息: {version_info}")
    
    # 字符串加密解密示例
    print("\n2. 字符串加密解密示例")
    
    # 测试数据
    test_cases = [
        ("Hello, World!", "simple_key"),
        ("哈吉咪加密解密器测试", "chinese_key"),
        ("This is a longer text with numbers 123456 and symbols !@#$%^&*()", "complex_key"),
        ("", "empty_test"),  # 空字符串测试
    ]
    
    for i, (plaintext, key) in enumerate(test_cases, 1):
        print(f"\n   测试案例 {i}:")
        print(f"   原文: '{plaintext}'")
        print(f"   密钥: '{key}'")
        
        try:
            if not plaintext:  # 空字符串应该抛出异常
                try:
                    encrypted = crypto.encrypt_string(plaintext, key)
                    print("   ✗ 空字符串加密应该失败但却成功了")
                except ValueError as e:
                    print(f"   ✓ 空字符串加密正确地失败了: {e}")
                continue
                
            # 加密
            encrypted = crypto.encrypt_string(plaintext, key)
            print(f"   密文: {encrypted[:50]}{'...' if len(encrypted) > 50 else ''}")
            
            # 解密
            decrypted = crypto.decrypt_string(encrypted, key)
            print(f"   解密: '{decrypted}'")
            
            # 验证结果
            if decrypted == plaintext:
                print("   ✓ 加密解密成功!")
            else:
                print("   ✗ 加密解密失败!")
                
        except Exception as e:
            print(f"   ✗ 发生错误: {e}")
    
    # 文件加密解密示例
    print("\n3. 文件加密解密示例")
    
    # 创建测试文件
    test_content = """这是一个测试文件。
It contains both Chinese and English text.
包含中英文混合内容。

数字: 1234567890
符号: !@#$%^&*()
特殊字符: αβγδε

文件加密解密测试完成。"""
    
    test_file = "test_input.txt"
    encrypted_file = "test_encrypted.dat"
    decrypted_file = "test_decrypted.txt"
    
    try:
        # 写入测试文件
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        print(f"   ✓ 创建测试文件: {test_file}")
        
        # 加密文件
        file_key = "file_encryption_key_2024"
        success = crypto.encrypt_file(test_file, encrypted_file, file_key)
        if success:
            print(f"   ✓ 文件加密成功: {encrypted_file}")
            
            # 检查加密文件大小
            encrypted_size = os.path.getsize(encrypted_file)
            print(f"   加密文件大小: {encrypted_size} 字节")
            
            # 解密文件
            success = crypto.decrypt_file(encrypted_file, decrypted_file, file_key)
            if success:
                print(f"   ✓ 文件解密成功: {decrypted_file}")
                
                # 验证文件内容
                with open(decrypted_file, 'r', encoding='utf-8') as f:
                    decrypted_content = f.read()
                
                if decrypted_content == test_content:
                    print("   ✓ 文件内容验证成功!")
                else:
                    print("   ✗ 文件内容验证失败!")
                    print("   原始内容长度:", len(test_content))
                    print("   解密内容长度:", len(decrypted_content))
            else:
                print("   ✗ 文件解密失败!")
        else:
            print("   ✗ 文件加密失败!")
            
    except Exception as e:
        print(f"   ✗ 文件操作发生错误: {e}")
    finally:
        # 清理测试文件
        for filename in [test_file, encrypted_file, decrypted_file]:
            try:
                if os.path.exists(filename):
                    os.remove(filename)
                    print(f"   清理文件: {filename}")
            except Exception:
                pass
    
    # 错误处理示例
    print("\n4. 错误处理示例")
    
    try:
        # 测试错误的密钥
        original = "测试错误密钥"
        encrypted = crypto.encrypt_string(original, "correct_key")
        decrypted = crypto.decrypt_string(encrypted, "wrong_key")
        print(f"   ✗ 错误密钥解密应该失败但却得到: '{decrypted}'")
    except Exception as e:
        print(f"   ✓ 错误密钥正确地导致了异常: {e}")
    
    try:
        # 测试无效的Base64
        crypto.decrypt_string("这不是有效的Base64编码", "any_key")
        print("   ✗ 无效Base64解密应该失败但却成功了")
    except Exception as e:
        print(f"   ✓ 无效Base64正确地导致了异常: {e}")
    
    print("\n" + "=" * 50)
    print("✓ 基本使用示例演示完成!")

if __name__ == "__main__":
    main()