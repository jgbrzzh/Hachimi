"""
created by: zzh 2025-09-23


from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)#导致奇怪的bug，弃用
#update:奇怪的bug是因为模块(python文件)在被引用时，会自动运行该模块(python文件)代码，导致重复执行

print(sys.path)
将工作目录改为源代码根目录，这里每一个.parent就是向上翻一级，sys.path[0]就是当前目录
"""
import sys
import os


def get_file_v2(): #获取文件路径的函数(可以根据调用方式，返回不同的路径)
    #下边这行放到函数里边是为了防止该语句在其所处模块(python文件)被引用时就执行从而导致奇怪的bug
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))#使下一个import能够找到PreProcess模块
    #python import模块时，是在sys.path里按顺序查找的。
    #sys.path是一个列表，里面以字符串的形式存储了许多路径。
    from PreProcess.FilePreProcess import get_filepath
    current_dir, project_root, toprocess_dir = get_filepath()
    if(is_import_by_main):#检测是否被主程序调用
        print("当前GetFilepath模块被主程序调用")
        print(f"当前目录(即主程序所在目录): {current_dir}")
        print(f"项目根目录: {project_root}")
    else:
        print(f"当前目录: {current_dir}")
        print(f"代码根目录: {project_root}")

#get_file_v2() 模块(python文件)在被引用时，会自动运行所有代码，导致重复执行

# 移除自动执行，只在被主动调用时运行
if __name__ == "__main__":
    is_import_by_main = False
    get_file_v2()



