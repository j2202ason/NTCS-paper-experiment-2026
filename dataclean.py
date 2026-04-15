import os
import shutil

def clear_files_in_folder(folder_path, exclude_extensions=None, exclude_names=None):
    if exclude_extensions is None:
        exclude_extensions = []
    if exclude_names is None:
        exclude_names = []

    if not os.path.exists(folder_path):
        print(f"Warning '{folder_path}' not exist")
        return

    if not os.path.isdir(folder_path):
        print(f"error: '{folder_path}' not a folder")
        return

    files_removed = 0
    files_skipped = 0

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            skip_file = False
            file_ext = os.path.splitext(file)[1].lower()
            if exclude_extensions and file_ext in exclude_extensions:
                skip_file = True

            if exclude_names and file.lower() in [name.lower() for name in exclude_names]:
                skip_file = True

            if skip_file:
                files_skipped += 1
                continue

            try:
                os.remove(file_path)
                files_removed += 1
                print(f"delete success: {file_path}")
            except Exception as e:
                print(f"delete fail {file_path}: {e}")

def clear_files_in_folder_simple(folder_path):
    if not os.path.exists(folder_path):
        print(f"folder '{folder_path}' not exist")
        return

    if not os.path.isdir(folder_path):
        print(f"'{folder_path}' not a folder")
        return

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
                print(f"delete: {file_path}")
            except Exception as e:
                print(f"delete fail {file_path}: {e}")


# 使用示例
def clean(fpath):
    clear_files_in_folder(
        fpath,
        exclude_extensions=['.txt', '.py','png','xlsx'],
        exclude_names=['readme.md', 'config.ini']
    )

    clear_files_in_folder(fpath)
    clear_files_in_folder_simple(fpath)