import base64
from datetime import datetime
import os
import time
import json
import random
import platform
import requests
import pandas as pd
from pathlib import Path
from selenium import webdriver
from collections import defaultdict
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from pynput.keyboard import Key as PyKey, Controller

from dotenv import load_dotenv
from pprint import pprint

from bake_notebook import IPYNBGenerator
from utils import GPTSpecificTextInLastElement, ensure_directory_exists


# Load environment variables from .env file
load_dotenv()

with open('jobs.json', 'r') as jfp:
    JOBS = json.loads(jfp.read())

pprint(JOBS)

try:
    with open('gpt-outputs.json', 'r') as of:
        OUTPUT = defaultdict(list, json.loads(of.read())) # Convert to defaultdict type
except Exception:
    OUTPUT = defaultdict(list)

RATER_ID = JOBS['rater_id']

print(platform.system())
print(platform.machine())

def get_chromedriver_path():
    # Supports linux64, mac-arm64, mac-x64, win32 and win64 arc
    system = platform.system()
    arch = platform.machine()
    
    if system == "Linux":
        return "webdrivers/chromedriver-linux64"
    elif system == "Darwin":
        if arch == "arm64":
            return "webdrivers/chromedriver-mac-arm64"
        else:
            return "webdrivers/chromedriver-mac-x64"
    elif system == "Windows":
        if arch.endswith("64"):
            return "webdrivers/chromedriver-win64.exe"
        else:
            return "webdrivers/chromedriver-win32.exe"
    else:
        raise Exception("Unsupported operating system")


# Initialize WebDriver with the appropriate ChromeDriver
chromedriver_path = get_chromedriver_path()
print('Chrome Driver Path:', chromedriver_path)

# Configure Chrome options
options = Options()
options.add_experimental_option("debuggerAddress", "localhost:9333") # Your GPT's chrome profile port would be on port "9222"
options.add_argument("--disable-blink-features=AutomationControlled")

# Function to introduce random delays
def random_delay(a=2, b=5):
    time.sleep(random.uniform(a, b))

# Initialize WebDriver with the appropriate ChromeDriver
service = ChromeService(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)


# Open a new session and run all prompts for each task/job
for task in JOBS['tasks']:
    task_id        = task['task_id']
    prompt_files   = task['files']
    files_uploaded = False

    if len(task['prompts']) >= 1: # Continue if prompts are available
        # Ensure the output directory exists
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(base_dir, 'notebooks', f"ID_{task_id}")
        ensure_directory_exists(output_dir)

        print(f'[x] Started Task ID: {task_id}.')

        # Open GPT
        driver.get('https://chatgpt.com/')

        for idx, user_query in enumerate(task['prompts']):
            print(f'[x] {task_id} - Starting Prompt {idx+1}: {user_query}')
            # Find the input text field elem
            input_text_elem_xpath = '//*[@id="prompt-textarea"]'
            WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, input_text_elem_xpath)))

            # Generate full path to all prompt files
            files_str = list(map(lambda x: str(Path(x).resolve()), prompt_files))

            prompt_elem = driver.find_element(By.XPATH, input_text_elem_xpath)
            prompt_elem.send_keys(user_query)

            # Find the file input element by its name or ID
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, input_text_elem_xpath)))
            # is_first_file = True

            # Ensures all files are uploaded just once.
            if not files_uploaded:
                for file in files_str:
                    upload_files_elem_xpath = '//*[@id="__next"]/div[1]/div[2]/main/div[1]/div[2]/div[1]/div/form/div/div[2]/div/div/div[1]/div/button[2]'
                    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, upload_files_elem_xpath)))
                    driver.find_element(By.XPATH, upload_files_elem_xpath).click()

                    upload_local_file_xpath = '//*[@id="radix-:ra:"]/div[4]'
                    try:
                        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, upload_local_file_xpath)))
                    except Exception:
                        upload_local_file_xpath = '//*[@id="radix-:rb:"]/div[4]'
                        try:
                            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, upload_local_file_xpath)))
                        except Exception:
                            upload_local_file_xpath = '//*[@id="radix-:r9:"]/div[4]'
                            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, upload_local_file_xpath)))
                    # //*[@id="radix-:rb:"]/div[4]
                    local_file_input = driver.find_element(By.XPATH, upload_local_file_xpath)
                    local_file_input.click() 

                    time.sleep(3)
                    keyboard = Controller()
                    keyboard.type(file)
                    keyboard.press(PyKey.enter)
                    keyboard.release(PyKey.enter)
                    is_first_file = False
                    print(f'[x] Prompt {idx+1}: File Uploaded Successfully! - {file}')

                # Make sure script doesn't attempt to upload files again.
                files_uploaded = True
                time.sleep(3)

            # Submit the query.
            submit_prompt_btn_xpath = '//*[@id="__next"]/div[1]/div[2]/main/div[1]/div[2]/div[1]/div/form/div/div[2]/div/div/button'

            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, submit_prompt_btn_xpath)))

            submit_prompt_btn = driver.find_element(By.XPATH, submit_prompt_btn_xpath)
            submit_prompt_btn.click()

            # Define the locator for the element you want to observe
            observed_element_locator = (By.CSS_SELECTOR, '[class*="group/conversation-turn"][class*="agent-turn"]')
            start_time = time.time()

            # Wait for the element to be present
            WebDriverWait(driver, 30).until(EC.presence_of_element_located(observed_element_locator))


            # Continue to wait for the specific text "Analyzed"
            WebDriverWait(driver, 120).until(GPTSpecificTextInLastElement(
                observed_element_locator, 
                "Analyzed", 
                idx+1,
                turn_menu_item_locator = (By.XPATH, './/div[contains(@class, "mt-1") and contains(@class, "flex") and contains(@class, "gap-3") and contains(@class, "empty:hidden") and contains(@class, "juice:-ml-3")]')
                ))

            # Record the time when "Analysis complete" appears
            analysis_complete_time = time.time()
            end_to_end_time = round(analysis_complete_time - start_time, 2)
            print(f"[x] Prompt {idx+1} End To End Time: {end_to_end_time} seconds")

            elements = driver.find_elements(*observed_element_locator)
            if elements:
                gpt_reponse_elem = elements[-1]
            else:
                gpt_reponse_elem = None

            # Ensure the bot is truly done with analysis by looking for the 
            # menu popup that every completed conversation has
            turn_menu_item_locator = (By.XPATH, './/div[contains(@class, "mt-1") and contains(@class, "flex") and contains(@class, "gap-3") and contains(@class, "empty:hidden") and contains(@class, "juice:-ml-3")]')
            WebDriverWait(gpt_reponse_elem, 120).until(EC.presence_of_element_located(turn_menu_item_locator))

            # Grab all GPT code and text response blocks while maintaining order
            response_blocks = gpt_reponse_elem.find_elements(By.XPATH, './/div[(normalize-space(@class) = "overflow-hidden") or @data-message-author-role="assistant"]')
            # Sort in the order they appear on screen
            response_blocks = sorted(response_blocks, key=lambda x: x.location['y'])

            # Find all img elements within the response element that have the ngcontent attribute
            plot_images = gpt_reponse_elem.find_elements(By.TAG_NAME, 'img')
            plot_images = [i for i in plot_images if str(i.get_attribute('alt')).lower().strip() == "output image"]

            if plot_images:
                # Iterate through each plot image and save it
                for img_idx, img in enumerate(plot_images):
                    # Get the src attribute, which contains the base64 encoded image
                    src = img.get_attribute('src')

                    # Download the image
                    response = requests.get(src)

                    file_path = os.path.join(output_dir, f'GPT_userquery{idx+1}_plot{img_idx+1}.png')

                    # Save the image to the specified path
                    with open(file_path, 'wb') as file:
                        file.write(response.content)

                time.sleep(3)
            else:
                plot_images = gpt_reponse_elem.find_elements(By.XPATH, '''
                    .//div[
                        @class = "mb-3 max-w-[80%]"
                    ]
                ''')
                print('[x] Found', len(plot_images), 'Images')

                if plot_images:
                    for img_idx, img in enumerate(plot_images):
                        file_path = os.path.join(output_dir, f'GPT_userquery{idx+1}_plot{img_idx+1}.png')
                        img.screenshot(file_path)
                    time.sleep(3)

            # Create and cleanup notebook string
            notebook_str = """"""
            for blk in response_blocks:
                try:
                    code_element = blk.find_element(By.TAG_NAME, 'code')
                    # Access the content of the <code> element
                    code_content = code_element.text.strip()
                    code_content = code_content.replace("\n", "\r\n")
                    notebook_str += f"```python?code_reference&code_event_index=2\r\n{code_content}\r\n```"

                except:
                    # print('No nested <code> element found.')
                    blk_text = blk.text.strip()
                    blk_text = blk_text.replace("\n", "\r\n")
                    notebook_str += f"```text?code_stdout&code_event_index=3\r\n{blk_text}\r\n```"
                
            OUTPUT[task_id].append({
                'prompt': user_query,
                'end_to_end_time': end_to_end_time,
                'response': notebook_str,
                'prompt_files': prompt_files
            })
            
            # Create local update/backup
            with open('gpt-outputs.json', 'w') as out:
                out.write(json.dumps(OUTPUT))

            df = pd.DataFrame({
                'rater_id': RATER_ID,
                'task_id': task_id,
                'prompt': user_query,
                'time_to_ice': 0,
                'end_to_end_time': end_to_end_time,
                'prompt_files': ",".join([f.split('/')[-1] for f in prompt_files]),
                'timestamp': datetime.now()
            })
            ensure_directory_exists('time-tracksheet/')
            df.to_csv('time-tracksheet/gpt-prompts-time-track-sheet.csv', mode='a', index=False, header=False)

        # Instantiate class for generating notebook after all prompts are done
        ipynb_gen = IPYNBGenerator(
            output_path = output_dir,
            rater_id    = RATER_ID,
            task_id     = task_id,
            nb_for="GPT" # Need to override this from "Gemini" to "GPT"
        )

        # Generate notebook
        ipynb_gen.text_to_notebook(
            OUTPUT[task_id]
        )
        print(f'[x] Completed Task ID: {task_id}.')







'''
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9333 --user-data-dir="C:\selenium_chrome_profile_2"

/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9333 --user-data-dir="/Users/<your-username>/selenium_chrome_profile_2"

google-chrome --remote-debugging-port=9333 --user-data-dir="/home/<your-username>/selenium_chrome_profile_2"

'''