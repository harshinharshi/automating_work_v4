from chatgpt import gpt_run
from gemini import gemini_run
import json
import pandas as pd

# df = pd.read_csv(r'c:\\Users\\harsh\\Downloads\\Test - Sheet1.csv')
df = pd.read_csv(r"C:\\Users\\harsh\\OneDrive\\Desktop\\Test - Sheet1.csv")

print("starting the process...")
# Convert each row to a list, combine the last two elements into a sublist, and modify the second element
rows_list = []
for index, row in df.iterrows():
    row_list = row.tolist()[:-2] + [row.tolist()[-2:]]
    # row_list[1] = "datasets\\" + str(row_list[1])  # Adding "datasets\\" in front of the second element
    rows_list.append(row_list)



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

# for i in rows_list:
#     print("\n row id :" ,i[0])
#     write_job_json(i)
#     print("entering GPT")
#     gpt_run()
#     print("exiting GPT")
#     print("\n completed row id :" ,i[0])

print("entering gemini")
for i in rows_list:
    write_job_json(i)
    print("entering geminin")
    gemini_run()
    print("exiting geminin")
print("done")