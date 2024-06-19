import os
import psutil
# close all the windows
# def close_chrome_windows():
#     try:
#         os.system("taskkill /im chrome.exe /f")
#         print("Chrome browser closed successfully.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# close_chrome_windows()

#  close only the chatgpt using chrome or the port 9333 opened chrome

def close_chrome_on_port_windows(port):
    try:
        # Iterate over all processes
        for proc in psutil.process_iter(['pid', 'name', 'connections']):
            if proc.info['name'] == 'chrome.exe':
                for conn in proc.info['connections']:
                    if conn.laddr.port == port:
                        os.system(f"taskkill /PID {proc.info['pid']} /F")
                        print(f"Closed Chrome process with PID {proc.info['pid']} on port {port}.")
                        return
        print(f"No Chrome process found on port {port}.")
    except Exception as e:
        print(f"An error occurred: {e}")



