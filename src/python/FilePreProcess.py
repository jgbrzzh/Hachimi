import os
def get_filepath(file_path):
    for root, dirs, files in os.walk(file_path):
        for file in files:
            file_path = os.path.join(root, file)
            preprocess_file(file_path)
def preprocess_file(file_path):
