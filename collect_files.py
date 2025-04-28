import os
import sys
import shutil

input_directory = sys.argv[1]
output_directory = sys.argv[2]

max_depth = 1
if len(sys.argv) >= 4:
    max_depth = int(sys.argv[3]) - 1

os.makedirs(output_directory, exist_ok=True)

for curr_dir, folder, name in os.walk(input_directory):
    rel_path = os.path.relpath(curr_dir, input_directory)

    if rel_path == ".":
        depth = 0
    else:
        depth = rel_path.count(os.sep) + 1

    if max_depth != 1 and depth > max_depth:
        folder.clear()
        continue

    list_of_folders = []
    if max_depth != 1:
        list_of_folders = rel_path.split(os.sep)[:max_depth]
    else:
        list_of_folders = rel_path.split(os.sep)

    if len(list_of_folders) > 0:
        short_path = os.path.join(*list_of_folders)
    else:
        short_path = "."

    last_folder = output_directory
    if short_path != ".":
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

        shutil.copy2(path_to_prev_file, target_file)
