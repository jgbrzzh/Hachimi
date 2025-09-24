#from .FilePreProcess import main_FileProProcess
from . import FilePreProcess

def main_FileProProcess_run():
    FilePreProcess.is_import_by_main = is_import_by_main  # 告诉FilePreProcess模块它是否被主程序调用的
    FilePreProcess.main_FileProProcess()

if __name__ == "__main__":
    is_import_by_main = False
    main_FileProProcess_run()