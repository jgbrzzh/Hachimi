#!/usr/bin/env python3
# 测试 Config 和 GetFile 模块的调试状态同步

import sys
import os
from pathlib import Path

# 添加src目录到sys.path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# 导入相关模块
import Config.Config as Config
import GetFilepath.GetFile as GetFile

def test_debug_sync():
    print("=== 测试调试状态同步 ===")
    
    # 1. 检查初始状态
    print(f"初始 Config.is_debug: {Config.is_debug}")
    
    # 2. 更改debug状态为True
    print("\n调用 Config.change_debug(True)...")
    Config.change_debug(True)
    print(f"Config.is_debug现在是: {Config.is_debug}")
    
    # 3. 调用GetFile.get_file_v2()查看debug状态
    print("\n调用 GetFile.get_file_v2()...")
    try:
        current_dir, project_root, toprocess_dir = GetFile.get_file_v2()
        print(f"返回值: current_dir={current_dir}")
    except Exception as e:
        print(f"执行出错: {e}")
    
    # 4. 再次更改debug状态为False
    print(f"\n调用 Config.change_debug(False)...")
    Config.change_debug(False)
    print(f"Config.is_debug现在是: {Config.is_debug}")
    
    # 5. 再次调用GetFile.get_file_v2()查看debug状态
    print("\n再次调用 GetFile.get_file_v2()...")
    try:
        current_dir, project_root, toprocess_dir = GetFile.get_file_v2()
        print(f"返回值: current_dir={current_dir}")
    except Exception as e:
        print(f"执行出错: {e}")

if __name__ == "__main__":
    test_debug_sync()