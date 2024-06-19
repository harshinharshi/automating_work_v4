from chatgpt import gpt_run
from gemini import gemini_run
import json
import pandas as pd
from close_chrome import close_chrome_on_port_windows
from reading_from_excel import reading_the_excel_file

file_path = r"C:\\Users\\harsh\\OneDrive\\Desktop\\test.xlsx"
path_from_excel = {'fictional_character_battles_complex.csv' : 'https://drive.google.com/file/d/1RHpV_YWXJ41fidiTLuqLzmKiQgMKNCnT/view?usp=sharing',
                   'manufacturing_defect_dataset.csv' : 'https://drive.google.com/file/d/1OgOQk1WNWCRHYE4iFiQB9ZHs9PrktKz-/view?usp=sharing',
                   'Student_performance_data _.csv' : 'https://drive.google.com/file/d/1DUoGIfsP_mLzV-oS421oe51lIhDvZrdI/view?usp=drive_link'
}


rows_list = reading_the_excel_file(file_path, path_from_excel)



def write_job_json(i):
    with open(f'./jobs.json', 'w+') as f:

        json_data =   {
        "rater_id": "122", 
        "tasks": [
            {
                "task_id": i[0], 
                "files": [
                    {
                        "path": i[1],
                        "url": i[2]
                    }
                    
                ],
                "prompts": i[3]
            }
        ]
        }
        f.write(json.dumps(json_data))

print("entering Gpt")
for i in rows_list:
    print("\n row id :" ,i[0])
    write_job_json(i)
    print("entering GPT")
    gpt_run()
    print("exiting GPT")
    print("\n completed row id :" ,i[0])

#  clossing gpt window
close_chrome_on_port_windows(9333)

print("entering gemini")
for i in rows_list:
    print("\n row id :" ,i[0])
    write_job_json(i)
    print("entering geminin")
    gemini_run()
    print("exiting geminin")
    print("\n completed row id :" ,i[0])
print("done")