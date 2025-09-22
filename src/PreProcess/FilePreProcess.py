import os
import shutil
from pathlib import Path

def get_filepath():
    current_dir = Path.cwd()
    project_root = current_dir.parent  # 从 src 回到 Hachimi
    toprocess_dir = project_root / "ToProcess"
    return current_dir,project_root,toprocess_dir

def print_and_get_filepath():
    current_dir,project_root,toprocess_dir = get_filepath()
    print(f"当前目录: {current_dir}")
    print(f"项目根目录: {project_root}")
    print(f"ToProcess目录: {toprocess_dir}")
    return current_dir,project_root,toprocess_dir

def pre_get_filepath_and_process():
    current_dir,project_root,toprocess_dir = print_and_get_filepath()
    
    if not toprocess_dir.exists():
        print(f"ToProcess文件夹不存在: {toprocess_dir}")
        return
    get_filepath_and_process(toprocess_dir, project_root)

def get_filepath_and_process(source_folder, project_root):
    processed_count = 0
    error_count = 0
    temp_dir = project_root / "temp"

    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"临时文件夹: {temp_dir}")
    print("-" * 50)
    
    for root, dirs, files in os.walk(source_folder):
        # 排除temp目录，避免递归处理
        dirs[:] = [d for d in dirs if d != 'temp']
        
        for file in files:
            full_file_path = os.path.join(root, file)
            try:
                preprocess_file(full_file_path, source_folder, temp_dir)
                processed_count += 1
            except Exception as e:
                error_count += 1
                print(f"处理失败: {file} - {e}")
    
    print("-" * 50)
    print(f"处理完成！成功: {processed_count}, 失败: {error_count}")
    print(f"文件保存在: {temp_dir}")


def preprocess_file(file_path, source_folder, temp_dir):

    try:
        source_path = Path(file_path)

        relative_path = source_path.relative_to(source_folder)

        target_path = temp_dir / relative_path

        target_path.parent.mkdir(parents=True, exist_ok=True)

        convert_to_utf8(str(source_path), str(target_path))
        
        print(f"已处理: {relative_path}")
        
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")


def convert_to_utf8(source_file, target_file):
    detected_encoding = detect_file_encoding(source_file)

    try:
        with open(source_file, 'r', encoding=detected_encoding, errors='replace') as f:
            content = f.read()
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"编码转换: {os.path.basename(source_file)} ({detected_encoding} -> UTF-8)")

    except (UnicodeDecodeError, UnicodeError):
        shutil.copy2(source_file, target_file)
        print(f"二进制文件直接复制: {os.path.basename(source_file)}")


def detect_file_encoding(file_path):
    import chardet

    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)
            result = chardet.detect(raw_data)
            encoding = result['encoding']

            encoding_map = {
                'GB2312': 'gbk',
                'GBK': 'gbk',
                'UTF-8-SIG': 'utf-8-sig',
                'UTF-8': 'utf-8',
                'ASCII': 'utf-8'
            }

            return encoding_map.get(encoding, encoding or 'utf-8')

    except Exception:
        return 'utf-8'
def main_FileProProcess():
    pre_get_filepath_and_process()

if __name__ == "__main__":
    main_FileProProcess()