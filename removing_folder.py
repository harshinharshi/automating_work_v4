import os
import shutil

def remove_directory():
    # remvoing notebook and the timestamp
    folder_paths = [r'C:\\work\\automating_work_v4\\notebooks', r'C:\\work\\automating_work_v4\\time-tracksheet']

    for folder_path in folder_paths:
        # Check if the folder exists
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # Remove the folder and all its contents
            shutil.rmtree(folder_path)
            print(f"Folder '{folder_path}' has been removed.")
        else:
            print(f"Folder '{folder_path}' does not exist.")