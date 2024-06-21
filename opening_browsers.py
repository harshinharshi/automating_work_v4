import subprocess
import time

# Path to the batch file
batch_file_path = r'C:\\work\\automating_work_v4\\opening_shell_script.sh'

def open_chrome_with_shell():
    # Execute the shell script to open Chrome instances
    subprocess.run(['sh', batch_file_path])
    # Wait a bit to ensure the shell commands have executed
    time.sleep(5)

    print("Chrome instances are opened. Continuing with the program...")

    