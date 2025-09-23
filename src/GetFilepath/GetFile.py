"""
from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)#导致奇怪的bug，弃用
print(sys.path)
将工作目录改为源代码根目录，这里每一个.parent就是向上翻一级，sys.path[0]就是当前目录
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),".."))

def get_file_v2():
    from PreProcess.FilePreProcess import get_filepath
    current_dir, project_root, toprocess_dir = get_filepath()
    print(f"当前目录: {current_dir}")
    print(f"代码根目录: {project_root}")

get_file_v2()


