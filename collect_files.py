import os
import sys
import shutil

input_directory = sys.argv[1]
output_directory = sys.argv[2]

max_depth = None
if len(sys.argv) >= 4:
    max_depth = int(sys.argv[3]) - 1

os.makedirs(output_directory, exist_ok=True)

for curr_dir, folder, name in os.walk(input_directory):
    rel_path = os.path.relpath(curr_dir, input_directory)
    
    curr_dir = rel_path.count(os.sep)
    if rel_path == '.':
        curr_dir = 0
    
    if max_depth is not None and curr_dir > max_depth:
        continue
    
    list_of_folders = []
    if max_depth is not None:
        list_of_folders = rel_path.split(os.sep)[:max_depth]
    else:
        list_of_folders = rel_path.split(os.sep)
    
    short_path = os.sep.join(list_of_folders) if list_of_folders else '.'
    
    last_folder = output_directory
    if short_path != '.':
        last_folder = os.path.join(output_directory, short_path)
    
    os.makedirs(last_folder, exist_ok=True)
    
    for filename in sorted(name):
        path_to_prev_file = os.path.join(curr_dir, filename)
        base_name, ext = os.path.splitext(filename)
        target_file = os.path.join(last_folder, filename)
        
        counter = 1
        while os.path.isfile(target_file):
            new_name = f"{base_name}_{counter}{ext}"
            target_file = os.path.join(last_folder, new_name)
            counter += 1
        
        shutil.copy(path_to_prev_file, target_file)