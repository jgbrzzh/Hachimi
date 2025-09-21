#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈吉咪加密解密器性能基准测试

这个脚本测试加密解密操作的性能，生成基准数据。
"""

import os
import sys
import time
import tempfile
import statistics
from typing import List, Tuple

# 添加src路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'python'))

try:
    from hachimi import HachimiCrypto
except ImportError:
    print("错误: 无法导入hachimi模块。请先运行构建命令。")
    sys.exit(1)

class PerformanceBenchmark:
    """性能基准测试类"""
    
    def __init__(self):
        """初始化基准测试"""
        self.crypto = HachimiCrypto()
        self.results = {}
    
    def time_function(self, func, *args, **kwargs) -> float:
        """计时函数执行时间"""
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        return end_time - start_time, result
    
    def benchmark_string_encryption(self, text_sizes: List[int], iterations: int = 10) -> None:
        """基准测试字符串加密"""
        print("\n📊 字符串加密性能测试")
        print("-" * 40)
        
        key = "benchmark_key_2024"
        
        for size in text_sizes:
            # 生成测试文本
            test_text = "A" * size
            
            encrypt_times = []
            decrypt_times = []
            
            for i in range(iterations):
                # 测试加密时间
                encrypt_time, encrypted = self.time_function(
                    self.crypto.encrypt_string, test_text, key
                )
                encrypt_times.append(encrypt_time)
                
                # 测试解密时间
                decrypt_time, decrypted = self.time_function(
                    self.crypto.decrypt_string, encrypted, key
                )
                decrypt_times.append(decrypt_time)
                
                # 验证正确性
                assert decrypted == test_text, f"解密验证失败，迭代 {i+1}"
            
            # 计算统计数据
            avg_encrypt = statistics.mean(encrypt_times)
            avg_decrypt = statistics.mean(decrypt_times)
            
            # 计算吞吐量 (MB/s)
            size_mb = size / (1024 * 1024)
            encrypt_throughput = size_mb / avg_encrypt if avg_encrypt > 0 else 0
            decrypt_throughput = size_mb / avg_decrypt if avg_decrypt > 0 else 0
            
            print(f"文本大小: {self.format_size(size)}")
            print(f"  加密时间: {avg_encrypt*1000:.2f} ms (吞吐量: {encrypt_throughput:.2f} MB/s)")
            print(f"  解密时间: {avg_decrypt*1000:.2f} ms (吞吐量: {decrypt_throughput:.2f} MB/s)")
            
            # 存储结果
            self.results[f"string_{size}"] = {
                'size': size,
                'encrypt_time': avg_encrypt,
                'decrypt_time': avg_decrypt,
                'encrypt_throughput': encrypt_throughput,
                'decrypt_throughput': decrypt_throughput
            }
    
    def benchmark_file_encryption(self, file_sizes: List[int], iterations: int = 5) -> None:
        """基准测试文件加密"""
        print("\n📊 文件加密性能测试")
        print("-" * 40)
        
        key = "file_benchmark_key_2024"
        
        with tempfile.TemporaryDirectory() as temp_dir:
            for size in file_sizes:
                input_file = os.path.join(temp_dir, f"test_{size}.dat")
                encrypted_file = os.path.join(temp_dir, f"encrypted_{size}.dat")
                decrypted_file = os.path.join(temp_dir, f"decrypted_{size}.dat")
                
                # 生成测试文件
                test_data = os.urandom(size)
                with open(input_file, 'wb') as f:
                    f.write(test_data)
                
                encrypt_times = []
                decrypt_times = []
                
                for i in range(iterations):
                    # 清理上次的文件
                    for f in [encrypted_file, decrypted_file]:
                        if os.path.exists(f):
                            os.remove(f)
                    
                    # 测试文件加密时间
                    encrypt_time, encrypt_success = self.time_function(
                        self.crypto.encrypt_file, input_file, encrypted_file, key
                    )
                    encrypt_times.append(encrypt_time)
                    assert encrypt_success, f"文件加密失败，迭代 {i+1}"
                    
                    # 测试文件解密时间
                    decrypt_time, decrypt_success = self.time_function(
                        self.crypto.decrypt_file, encrypted_file, decrypted_file, key
                    )
                    decrypt_times.append(decrypt_time)
                    assert decrypt_success, f"文件解密失败，迭代 {i+1}"
                    
                    # 验证文件内容
                    with open(decrypted_file, 'rb') as f:
                        decrypted_data = f.read()
                    assert decrypted_data == test_data, f"文件内容验证失败，迭代 {i+1}"
                
                # 计算统计数据
                avg_encrypt = statistics.mean(encrypt_times)
                avg_decrypt = statistics.mean(decrypt_times)
                
                # 计算吞吐量 (MB/s)
                size_mb = size / (1024 * 1024)
                encrypt_throughput = size_mb / avg_encrypt if avg_encrypt > 0 else 0
                decrypt_throughput = size_mb / avg_decrypt if avg_decrypt > 0 else 0
                
                print(f"文件大小: {self.format_size(size)}")
                print(f"  加密时间: {avg_encrypt:.3f} s (吞吐量: {encrypt_throughput:.2f} MB/s)")
                print(f"  解密时间: {avg_decrypt:.3f} s (吞吐量: {decrypt_throughput:.2f} MB/s)")
                
                # 存储结果
                self.results[f"file_{size}"] = {
                    'size': size,
                    'encrypt_time': avg_encrypt,
                    'decrypt_time': avg_decrypt,
                    'encrypt_throughput': encrypt_throughput,
                    'decrypt_throughput': decrypt_throughput
                }
    
    def benchmark_key_sizes(self) -> None:
        """测试不同密钥长度的性能影响"""
        print("\n📊 密钥长度性能测试")
        print("-" * 40)
        
        test_text = "A" * 10000  # 10KB测试文本
        key_lengths = [8, 16, 32, 64, 128, 256]
        iterations = 20
        
        for key_length in key_lengths:
            key = "k" * key_length
            
            times = []
            for _ in range(iterations):
                encrypt_time, encrypted = self.time_function(
                    self.crypto.encrypt_string, test_text, key
                )
                decrypt_time, decrypted = self.time_function(
                    self.crypto.decrypt_string, encrypted, key
                )
                times.append(encrypt_time + decrypt_time)
                
                assert decrypted == test_text, "密钥长度测试验证失败"
            
            avg_time = statistics.mean(times)
            print(f"密钥长度 {key_length:3d} 字符: {avg_time*1000:.2f} ms")
    
    def benchmark_different_data_types(self) -> None:
        """测试不同数据类型的性能"""
        print("\n📊 数据类型性能测试")
        print("-" * 40)
        
        key = "datatype_test_key"
        size = 10000
        iterations = 10
        
        test_cases = [
            ("纯ASCII", "A" * size),
            ("纯数字", "1234567890" * (size // 10)),
            ("纯中文", "中" * size),
            ("混合内容", "Hello世界123!@#" * (size // 15)),
            ("重复模式", "ABCD" * (size // 4)),
            ("随机字符", "".join(chr(i % 95 + 32) for i in range(size)))
        ]
        
        for data_type, test_text in test_cases:
            if len(test_text) < size:
                test_text = test_text * (size // len(test_text) + 1)
            test_text = test_text[:size]
            
            times = []
            for _ in range(iterations):
                encrypt_time, encrypted = self.time_function(
                    self.crypto.encrypt_string, test_text, key
                )
                decrypt_time, decrypted = self.time_function(
                    self.crypto.decrypt_string, encrypted, key
                )
                times.append(encrypt_time + decrypt_time)
                
                assert decrypted == test_text, f"{data_type}测试验证失败"
            
            avg_time = statistics.mean(times)
            compression_ratio = len(encrypted) / len(test_text.encode('utf-8'))
            
            print(f"{data_type:10s}: {avg_time*1000:.2f} ms (压缩比: {compression_ratio:.2f})")
    
    def format_size(self, size_bytes: int) -> str:
        """格式化文件大小显示"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/(1024**2):.1f} MB"
        else:
            return f"{size_bytes/(1024**3):.1f} GB"
    
    def generate_report(self) -> None:
        """生成性能报告"""
        print("\n📋 性能测试报告")
        print("=" * 50)
        
        print("\n🏆 最佳性能指标:")
        
        # 找出最高吞吐量
        max_encrypt_throughput = 0
        max_decrypt_throughput = 0
        best_encrypt_case = ""
        best_decrypt_case = ""
        
        for test_name, result in self.results.items():
            if result['encrypt_throughput'] > max_encrypt_throughput:
                max_encrypt_throughput = result['encrypt_throughput']
                best_encrypt_case = test_name
            
            if result['decrypt_throughput'] > max_decrypt_throughput:
                max_decrypt_throughput = result['decrypt_throughput']
                best_decrypt_case = test_name
        
        print(f"  最高加密吞吐量: {max_encrypt_throughput:.2f} MB/s ({best_encrypt_case})")
        print(f"  最高解密吞吐量: {max_decrypt_throughput:.2f} MB/s ({best_decrypt_case})")
        
        print(f"\n💻 测试环境:")
        print(f"  Python 版本: {sys.version}")
        print(f"  平台: {sys.platform}")
        
        # 获取系统信息
        try:
            import platform
            print(f"  CPU: {platform.processor()}")
            print(f"  系统: {platform.system()} {platform.release()}")
        except:
            pass

def main():
    """主函数"""
    print("🚀 哈吉咪加密解密器 - 性能基准测试")
    print("=" * 50)
    
    # 创建基准测试实例
    benchmark = PerformanceBenchmark()
    
    try:
        # 测试连接
        connection_result = benchmark.crypto.test_connection()
        print(f"C++模块连接: {connection_result}")
        
        # 字符串加密性能测试
        string_sizes = [1024, 10*1024, 100*1024, 1024*1024]  # 1KB, 10KB, 100KB, 1MB
        benchmark.benchmark_string_encryption(string_sizes)
        
        # 文件加密性能测试
        file_sizes = [1024*1024, 10*1024*1024]  # 1MB, 10MB
        benchmark.benchmark_file_encryption(file_sizes, iterations=3)
        
        # 密钥长度测试
        benchmark.benchmark_key_sizes()
        
        # 数据类型测试
        benchmark.benchmark_different_data_types()
        
        # 生成报告
        benchmark.generate_report()
        
        print("\n✅ 性能基准测试完成!")
        
    except Exception as e:
        print(f"\n❌ 性能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())