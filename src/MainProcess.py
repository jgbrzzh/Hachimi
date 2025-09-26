"""
created by: zzh 2025-09-21
"""





class MainProcess:
    def __init__(self):
        self.count = 0
        self.choice= None
        from PreProcess.FilePreProcess import get_filepath
        self.current_dir,self.project_root,self.toprocess_dir = get_filepath()

    def set_up_golbal(self):
        #import Config.Config

        """
        global Config.Config.is_import_by_main_v2
        global Config.Config.is_debug
        """
        import Config.Config
        #Config.Config.is_import_by_main_v2 = True  # 设定全局变量,表示被主程序调用
        Config.Config.change_import_by_main_v2(True)
        #Config.Config.is_debug = True  # 设定全局变量,表示是否开启调试模式
        Config.Config.change_debug(True)
        if(Config.Config.is_import_by_main_v2):
            print("从主程序启动")
        if(Config.Config.is_debug):
            print("开启调试模式")

    def print_menu(self):
        self.count += 1
        if self.count == 1:
            print("开始运行前请将要处理的文件放入ToProcess文件夹中，处理完成的文件会保存在Result文件夹中。")
        print("请选择要进行的操作:")
        print("1. 预处理文件 (转换为UTF-8编码)(已弃用)")
        print("2. 加密")
        print("3. 解密")
        print("4. 退出")

    def get_password(self):
        import Config.Config
        if (not Config.Config.password):
            password = input("请输入加密密码: ")
            Config.Config.change_password(password)
        else:
            print("已设置加密密码，是否继续使用该密码。")
            choice = input("输入 y 继续使用，其他键重新输入密码: ")
            if choice.lower() != 'y':
                password = input("请输入加密密码: ")
                Config.Config.change_password(password)

    def get_choice(self):
        self.print_menu()
        self.choice = input("输入选项编号 (1-4): ")

    def process_choice(self):
        #self.choice = input("输入选项编号 (1-4): ")
        #current_dir = Path.cwd()
        #print(current_dir)
        from PreProcess.FilePreProcessRunner import main_FileProProcess_run #弃用
        import PreProcess.FilePreProcessRunner
        PreProcess.FilePreProcessRunner.is_import_by_main = True #告诉FilePreProcessRunner模块它是被主程序调用的
        #current_dir = Path.cwd()
        #print(current_dir)
        #from GetFilepath.GetFile import get_file_v2 #弃用 改为直接导入整个模块
        import GetFilepath.GetFile
        GetFilepath.GetFile.is_import_by_main = True #告诉GetFile模块它是被主程序调用的
        if self.choice == '1':
            main_FileProProcess_run()
        elif self.choice == '2':
            #main_FileProProcess_run()
            #Config.Config.change_debug(True)
            """已解决：
            BUG：这里更新debug值，
            但是在GetFile模块中，print(f"Debug状态: {is_debug}")显示False
            原因：
            Config.Config 和 src.Config.Config 是两个不同的模块对象（不同的id）
            当我们通过 Config.Config.change_debug(True) 修改 Config.Config 的 is_debug 时，
            src.Config.Config 的 is_debug 仍然是 False
            在 sys.modules 中存在两个不同的模块实例
            详细可运行 test_debug_sync.py (BUG复现)
            test_debug_sync_fixed.py (BUG修复)
            debug_import.py (BUG究源)
            查看
            
            """
            import Config.Config
            if(Config.Config.is_debug):
                Config.Config.debug_info()
                Config.Config.config_info()
            self.get_password()
            from Config.Config import password
            if(Config.Config.is_debug):
                print(f"当前加密密码: {password}")

            #GetFilepath.GetFile.get_file_v2()
            if(not GetFilepath.GetFile.check_toprocess_exists_v2()):
                print("请先创建ToProcess文件夹并放入要处理的文件，然后重新运行程序。")
                return





        elif self.choice == '3':
            import Config.Config
            self.get_password()
        elif self.choice == '4':
            print("退出程序。")
            exit(0)
        else:
            print("无效选项，请重新选择。")
    def run(self):
        self.set_up_golbal()

        while True:
            self.get_choice()
            self.process_choice()

def main():
    main_Process = MainProcess()
    main_Process.run()
if __name__ == "__main__":
    main()