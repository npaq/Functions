import os

# Retrieving the list of a certain type of files inside the folder
def get_list_of_files(folder_path, file_type):
    files = [f for f in os.listdir(folder_path) 
        if os.path.isfile(os.path.join(folder_path,f))
        and f[-len(file_type)-1:] == '.' + file_type
        ]
    return files