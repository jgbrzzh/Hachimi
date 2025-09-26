def print_decorator(src_func):
    def wrapper(*args, **kwargs):
        current_dir, project_root, toprocess_dir = src_func(*args, **kwargs)
        from Config.Config import is_debug
        if(is_debug):
            if(is_import_by_main):#检测是否被主程序调用
                print("当前Decorator模块被主程序调用,正在执行print_decorator")
                print(f"当前目录(即主程序所在目录): {current_dir}")
                print(f"项目根目录: {project_root}")
            else:
                print("当前Decorator模块未被主程序调用,正在执行print_decorator")
                print(f"当前目录: {current_dir}")
                print(f"代码根目录: {project_root}")
        return current_dir, project_root, toprocess_dir
    return wrapper

def time_decorator(src_func):
    import time
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = src_func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"函数 {src_func.__name__} 执行时间: {elapsed_time:.4f} 秒")
        return result
    return wrapper
