import sys
import os
def Decode():
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    import GetFilepath.GetFile as GetFile
    import Config.Config as Config
    if (not GetFile.check_toprocess_exists_v2()):
        print("请先创建ToProcess文件夹并放入要处理的文件，然后重新运行程序。")
        return
    toprocess_dir = GetFile.get_toprocess_dir()
    all_file_paths = GetFile.get_all_file_paths(toprocess_dir)
    if (not all_file_paths):
        print("ToProcess文件夹中没有文件，请添加文件后重新运行程序。")
        return
    exe_path = GetFile.get_exe_path()
    GetFile.process_all_files(all_file_paths, "decode", exe_path)