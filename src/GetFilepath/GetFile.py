"""
from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)#导致奇怪的bug，弃用
print(sys.path)
将工作目录改为源代码根目录，这里每一个.parent就是向上翻一级，sys.path[0]就是当前目录
"""
import sys
import os


def get_file_v2():
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))#使下一个import生效
    from PreProcess.FilePreProcess import get_filepath
    current_dir, project_root, toprocess_dir = get_filepath()
    print(f"当前目录: {current_dir}")
    print(f"代码根目录: {project_root}")
#get_file_v2() 模块在被引用时，会自动运行所有代码，导致重复执行
# 移除自动执行，只在被主动调用时运行
if __name__ == "__main__":
    get_file_v2()


