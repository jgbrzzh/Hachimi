is_import_by_main_v2 = False  # 默认值，表示该模块未被主程序调用

is_debug = False  # 默认值，表示未开启调试模式


def change_import_by_main_v2(value: bool):
    global is_import_by_main_v2
    is_import_by_main_v2 = value
def change_debug(value: bool):
    global is_debug
    is_debug = value




