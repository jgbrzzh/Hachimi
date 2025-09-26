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
from pathlib import Path
from typing import Iterable, Optional, Union
import shutil
import subprocess



def get_file_v2(): #获取文件路径的函数(可以根据调用方式，返回不同的路径)
    #下边这行放到函数里边是为了防止该语句在其所处模块(python文件)被引用时就执行从而导致奇怪的bug

    #sys.path.append(os.path.join(os.path.dirname(__file__), ".."))#使下一个import能够找到PreProcess模块

    #python import模块时，是在sys.path里按顺序查找的。
    #sys.path是一个列表，里面以字符串的形式存储了许多路径。

    #from PreProcess.FilePreProcess import get_filepath



    #from src.Config.Config import is_debug


    #src.Config.Config.change_debug(True)
    
    # 导入Config模块获取最新配置 - 修复导入路径
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    # from src.PreProcess.FilePreProcess import get_filepath
    #修复导入路径
    from PreProcess.FilePreProcess import get_filepath
    import Config.Config
    is_debug = Config.Config.is_debug
    if is_debug:
        print(__file__)

    
    if(is_debug):
        #print("from src.PreProcess.FilePreProcess import get_filepath执行成功")
        pass
    current_dir, project_root, toprocess_dir = get_filepath()
    if is_debug:
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
    
    from Config.Config import is_debug
    from Config.Config import debug_info
    if(is_debug):
        debug_info()
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

"""
    def get_filepath_and_encode(source_folder, project_root): 被process_all_files替代
    # 导入Config模块获取最新配置 - 修复导入路径
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    import Config.Config
    is_import_by_main_v2 = Config.Config.is_import_by_main_v2
    
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
                #todo
                processed_count += 1
            except Exception as e:
                error_count += 1
                print(f"处理失败: {file} - {e}")

    print("-" * 50)
    print(f"处理完成！成功: {processed_count}, 失败: {error_count}")
    print(f"文件保存在: {temp_dir}")
    """

def get_project_root():

    project_root = Path(__file__).resolve()
    print(project_root)
    for _ in range(3):
        project_root = project_root.parent
    print(project_root)
    return project_root

def get_toprocess_dir():
    project_root = get_project_root()
    toprocess_dir = (project_root / "Toprocess").resolve()
    return toprocess_dir

def get_all_file_paths(
    source_folder,
    include_ext: Optional[Iterable[str]] = None,
    as_str: bool = False
):
    source_path = Path(source_folder).resolve()
    if not source_path.is_dir():
        raise NotADirectoryError(f"源目录不存在: {source_path}")

    if include_ext:
        include_set = {e.lower() for e in include_ext}
    else:
        include_set = None

    results: list[Path] = []
    for p in source_path.rglob("*"):
        if not p.is_file():
            continue
        if include_set and p.suffix.lower() not in include_set:
            continue
        results.append(p)

    return [str(p) for p in results] if as_str else results

def get_exe_path():
    project_root = get_project_root()
    exe_path = (project_root / "a.exe").resolve()
    if not exe_path.is_file():
        raise FileNotFoundError(f"C++ 可执行文件不存在: {exe_path}")
    return exe_path


def process_all_files(
        file_paths: Iterable[Union[str, Path]],
        format: str,
        cpp_exe: Union[str, Path],
):

    exe_path = Path(cpp_exe).resolve()
    if not exe_path.is_file():
        raise FileNotFoundError(f"C++ 可执行文件不存在: {exe_path}")

    success = 0
    failed_items: list[tuple[str, str]] = []

    for fp in file_paths:
        abs_path = Path(fp).resolve()
        if not abs_path.is_file():
            error_msg = "目标文件不存在"
            failed_items.append((str(abs_path), error_msg))
            print(f"失败: {abs_path} - {error_msg}")
            continue

        cmd = [str(abs_path), format]
        try:
            # 期望 C++ 程序: argv[1] = 文件路径, argv[2] = format
            print(f"处理中: {abs_path}")
            completed = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )
            if completed.returncode == 0:
                success += 1
                print(f"成功: {abs_path}")
            else:
                err_msg = (completed.stderr or completed.stdout or "").strip()
                error_info = f"returncode={completed.returncode} msg={err_msg}"
                failed_items.append((str(abs_path), error_info))
                print(f"失败: {abs_path} - {error_info}")

        except Exception as e:
            error_info = f"Exception: {e}"
            failed_items.append((str(abs_path), error_info))
            print(f"异常: {abs_path} - {error_info}")

    # 输出最终统计信息
    print(f"\n处理完成: 成功 {success} 个，失败 {len(failed_items)} 个")

    return failed_items



#get_file_v2() 模块(python文件)在被引用时，会自动运行所有代码，导致重复执行
# 移除自动执行，只在被主动调用时运行
if __name__ == "__main__":
    is_import_by_main = False
    get_file_v2()



