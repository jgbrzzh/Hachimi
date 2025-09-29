import inspect
from pathlib import Path

is_import_by_main_v2 = False  # 默认值，表示该模块未被主程序调用

is_debug = False  # 默认值，表示未开启调试模式

password = None

use_password = False

is_use_v2 = False

def debug_info():
    frame = inspect.currentframe().f_back
    file_name = Path(frame.f_code.co_filename).name
    func_name = frame.f_code.co_name  # 若在模块顶层会是 <module>
    print(f"由 {file_name} 输出，当前所在函数：{func_name}")

def config_info():
    print(f"Config模块: is_import_by_main_v2 = {is_import_by_main_v2}, is_debug = {is_debug}")

def change_is_use_v2(value: bool):
    global is_use_v2
    is_use_v2 = value

def change_password(pwd: str):
    global password
    password = pwd

def change_import_by_main_v2(value: bool):
    global is_import_by_main_v2
    is_import_by_main_v2 = value

def change_debug(value: bool):
    global is_debug
    is_debug = value




