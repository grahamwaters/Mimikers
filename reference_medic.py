import os
from tqdm import tqdm
import time
import re

def inner_matcher(file_ending, folder, line, f, pattern, is_jupyter=False):
    match = re.search(pattern, line)
    if match:
        filename = match.group()
        new_path = '../{}/{}'.format(folder,filename) if is_jupyter else './config/{}'.format(filename)
        # replace the path in the line with the new path and add the open statement
        f.write(line.replace(filename, new_path))
    else:
        f.write(line)

def update_paths(file_path, is_jupyter=False):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        return
    with open(file_path, 'w') as f:
        for line in lines: # for each line in the file
            # if the line is a comment skip it
            if line.startswith('#'):
                f.write(line)
                continue
            pattern = r'(?<=\().*?(?=[\'"])'
            if line.startswith('with'):
                match = re.search(pattern, line)
                if match:
                    filename = match.group()
                    new_path = '../config/{}'.format(filename) if is_jupyter else './config/{}'.format(filename)
                    # replace the path in the line with the new path and add the open statement
                    f.write(line.replace(filename, new_path))
                else:
                    f.write(line)
            # if json, or jsonl in the line then it goes in config folder
            if '.json' in line:
                inner_matcher('.json', 'config', line, f, pattern, is_jupyter)
            # if .txt in the line then it goes in data folder
            elif '.jsonl' in line:
                inner_matcher('.jsonl', 'config', line, f, pattern, is_jupyter)
            elif '.txt' in line:
                inner_matcher('.txt', 'data', line, f, pattern, is_jupyter)
            # if .csv in the line then it goes in data folder
            elif '.csv' in line:
                inner_matcher('.csv', 'data', line, f, pattern, is_jupyter)
            # if .png in the line then it goes in images folder
            elif '.png' in line:
                inner_matcher('.png', 'images', line, f, pattern, is_jupyter)
            # if .jpg in the line then it goes in images folder
            elif '.jpg' in line:
                inner_matcher('.jpg', 'images', line, f, pattern, is_jupyter)
            # if .jpeg in the line then it goes in images folder
            elif '.jpeg' in line:
                inner_matcher('.jpeg', 'images', line, f, pattern, is_jupyter)
            # if .gif in the line then it goes in images folder
            elif '.gif' in line:
                inner_matcher('.gif', 'images', line, f, pattern, is_jupyter)
            # if .svg in the line then it goes in images folder
            elif '.svg' in line:
                inner_matcher('.svg', 'images', line, f, pattern, is_jupyter)
            # if .ipynb in the line then it goes in notebooks folder
            elif '.ipynb' in line:
                inner_matcher('.ipynb', 'notebooks', line, f, pattern, is_jupyter)
            # if .py in the line then it goes in src folder
            elif '.py' in line:
                inner_matcher('.py', 'src', line, f, pattern, is_jupyter)



def scan_folder(folder_path):
    for dirpath, dirnames, filenames in tqdm(os.walk(folder_path), desc='Scanning folder'):
        for filename in tqdm(filenames, desc='\nUpdating file refs'):
            if filename == 'reference_medic.py':
                continue # skip this file
            print('\nUpdating file: {}  '.format(filename))
            #time.sleep(0.1)
            file_path = os.path.join(dirpath, filename)
            if '.ipynb' in file_path:
                is_jupyter = True
                update_paths(file_path, is_jupyter)
            elif '.py' in file_path:
                is_jupyter = False
                update_paths(file_path, is_jupyter)

def main():
    is_jupyter = False
    scan_folder('./')

if __name__ == '__main__':
    main()