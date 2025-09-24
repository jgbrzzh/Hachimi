#!/usr/bin/env python3
# 调试模块导入问题

import sys
import os
from pathlib import Path

# 添加src目录到sys.path
sys.path.insert(0, str(Path(__file__).parent / "src"))

print("sys.path:")
for i, path in enumerate(sys.path):
    print(f"  {i}: {path}")

print("\n=== 测试不同导入方式 ===")

# 方式1: 直接导入Config.Config
import Config.Config as Config1
print(f"方式1 - Config1.is_debug: {Config1.is_debug}")
print(f"方式1 - Config1模块路径: {Config1.__file__}")
import Config.Config as Config3
print(f"方式3 - Config3.is_debug: {Config1.is_debug}")
print(f"方式3 - Config3模块路径: {Config1.__file__}")

# 方式2: 导入src.Config.Config  
import src.Config.Config as Config2
print(f"方式2 - Config2.is_debug: {Config2.is_debug}")
print(f"方式2 - Config2模块路径: {Config2.__file__}")

# 检查是否是同一个对象
print(f"\n是否是同一个模块对象: {Config1 is Config2}")
print(f"Config1 id: {id(Config1)}")
print(f"Config2 id: {id(Config2)}")
print(f"Config3 id: {id(Config3)}")

# 测试修改一个是否影响另一个
print(f"\n修改前 - Config1.is_debug: {Config1.is_debug}, Config2.is_debug: {Config2.is_debug}")
Config1.change_debug(True)
print(f"通过Config1修改后 - Config1.is_debug: {Config1.is_debug}, Config2.is_debug: {Config2.is_debug}")

# 查看sys.modules中的模块
print(f"\nsys.modules中的相关模块:")
for module_name in sys.modules:
    if 'Config' in module_name:
        print(f"  {module_name}: {sys.modules[module_name]}")