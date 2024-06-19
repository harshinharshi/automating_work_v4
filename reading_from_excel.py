# file_path = r"C:\\Users\\harsh\\OneDrive\\Desktop\\test.xlsx"
# path_from_excel = {'fictional_character_battles_complex.csv' : 'https://drive.google.com/file/d/1RHpV_YWXJ41fidiTLuqLzmKiQgMKNCnT/view?usp=sharing',
#                    'manufacturing_defect_dataset.csv' : 'https://drive.google.com/file/d/1OgOQk1WNWCRHYE4iFiQB9ZHs9PrktKz-/view?usp=sharing'
# }



import pandas as pd

def reading_the_excel_file(file_path, path_from_excel):
    df = pd.read_excel(file_path)

    # Extracting relevant columns
    columns_to_extract = [
        'ID\n[Do Not Edit]', 'Input File(s)\nTurn 1', 'Prompt\nTurn 1', 
        'Input Files(s)\nTurn 2', 'Prompt\nTurn 2', 'Input Files(s)\nTurn 3', 
        'Prompt\nTurn 3', 'Input Files(s)\nTurn 4', 'Prompt\nTurn 4'
    ]
    extracted_df = df[columns_to_extract]

    # Combine prompts into a single column with elements enclosed in double quotes
    extracted_df['Combined Prompts'] = extracted_df[[f'Prompt\nTurn {turn}' for turn in range(1, 5)]].apply(
        lambda x: ', '.join(f'"{str(item).replace('"', "'")}"' for item in x.dropna()), 
        axis=1
    )

    # print()
    # for i in extracted_df['Combined Prompts']:
    #     print(i)

    # Create a list for each row using the specified columns and additional 'path' value
    def create_custom_list(row):
        combined_prompts_list = [item.strip('"').strip("'") for item in row['Combined Prompts'].split('", "')]
        combined_prompts_list[0] = combined_prompts_list[0].replace('"', '')  # Removing the starting quote from the first element
        combined_prompts_list[-1] = combined_prompts_list[-1].replace('"', '')  # Removing the ending quote from the last element
        return [
            row['ID\n[Do Not Edit]'],
            row['Input File(s)\nTurn 1'],
            path_from_excel[row['Input File(s)\nTurn 1']],
            combined_prompts_list
        ]

    # Applying the function to each row to create the list
    list_from_dataframe = extracted_df.apply(create_custom_list, axis=1).tolist()

    # for i in list_from_dataframe:
    #     print(i[-2])

    return list_from_dataframe


# reading_the_excel_file(file_path, path_from_excel)