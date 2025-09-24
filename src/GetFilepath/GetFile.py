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

    #sys.path.append(os.path.join(os.path.dirname(__file__), ".."))#使下一个import能够找到PreProcess模块

    #python import模块时，是在sys.path里按顺序查找的。
    #sys.path是一个列表，里面以字符串的形式存储了许多路径。

    #from PreProcess.FilePreProcess import get_filepath

    from src.PreProcess.FilePreProcess import get_filepath
    #from src.Config.Config import is_debug
    import src.Config.Config
    
    # 修复：在函数内部获取最新的is_debug值，而不是在模块导入时固定值
    is_debug = src.Config.Config.is_debug
    print(f"Debug状态: {is_debug}")
    
    if(is_debug):
        print("from src.PreProcess.FilePreProcess import get_filepath执行成功")
    current_dir, project_root, toprocess_dir = get_filepath()
    if(is_import_by_main):#检测是否被主程序调用
        print("当前GetFilepath模块被主程序调用，正在执行get_file_v2")
        print(f"当前目录(即主程序所在目录): {current_dir}")
        print(f"项目根目录: {project_root}")
    else:
        print("当前GetFilepath模块未被主程序调用，正在执行get_file_v2")
        print(f"当前目录: {current_dir}")
        print(f"代码根目录: {project_root}")
    return current_dir, project_root, toprocess_dir


def check_toprocess_exists_v2():
    current_dir, project_root, toprocess_dir = get_file_v2()
    

    if(is_import_by_main):#检测是否被主程序调用
        print("当前GetFilepath模块被主程序调用，正在执行check_toprocess_exists_v2")
        """
        print(f"当前目录(即主程序所在目录): {current_dir}")
        print(f"项目根目录: {project_root}")
        print(toprocess_dir)
        """
    else:
        print("当前GetFilepath模块未被主程序调用，正在执行check_toprocess_exists_v2")
        print(f"当前目录: {current_dir}")
        print(f"代码根目录: {project_root}")
    
    if not toprocess_dir.exists():
        print(f"ToProcess文件夹不存在: {toprocess_dir}")
        return False
    return True

def get_filepath_and_encode(source_folder, project_root):
    # 导入Config模块获取最新配置
    from src.Config.Config import is_import_by_main_v2
    # 导入预处理函数
    from src.PreProcess.FilePreProcess import preprocess_file
    
    if(is_import_by_main_v2):
        pass
    processed_count = 0
    error_count = 0
    temp_dir = project_root / "temp"

    for root, dirs, files in os.walk(source_folder):
        # 排除temp目录，避免递归处理
        dirs[:] = [d for d in dirs if d != 'temp']

        for file in files:
            full_file_path = os.path.join(root, file)
            try:
                # 使用正确的预处理函数
                preprocess_file(full_file_path, source_folder, temp_dir)
                processed_count += 1
            except Exception as e:
                error_count += 1
                print(f"处理失败: {file} - {e}")

    print("-" * 50)
    print(f"处理完成！成功: {processed_count}, 失败: {error_count}")
    print(f"文件保存在: {temp_dir}")

#get_file_v2() 模块(python文件)在被引用时，会自动运行所有代码，导致重复执行
# 移除自动执行，只在被主动调用时运行
if __name__ == "__main__":
    is_import_by_main = False
    get_file_v2()



