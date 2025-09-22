
class MainProcess:
    def __init__(self):
        self.count = 0
        self.choice= None
        from python.FilePreProcess import get_filepath
        self.current_dir,self.project_root,self.toprocess_dir = get_filepath()


    def print_menu(self):
        self.count += 1
        if self.count == 1:
            print("开始运行前请将要处理的文件放入ToProcess文件夹中，处理完成的文件会保存在Result文件夹中。")
        print("请选择要进行的操作:")
        print("1. 预处理文件 (转换为UTF-8编码)")
        print("2. 加密")
        print("3. 解密")
        print("4. 退出")

    def get_choice(self):
        self.print_menu()
        self.choice = input("输入选项编号 (1-4): ")

    def process_choice(self):
        if self.choice == '1':
            from python.FilePreProcessRunner import main_FileProProcess_run
            main_FileProProcess_run()
        elif self.choice == '2':
            pass
        elif self.choice == '3':
            pass
        elif self.choice == '4':
            print("退出程序。")
            exit(0)
        else:
            print("无效选项，请重新选择。")
    def run(self):
        while True:
            self.get_choice()
            self.process_choice()

def main():
    main_Process = MainProcess()
    main_Process.run()
if __name__ == "__main__":
    main()