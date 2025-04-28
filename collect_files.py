import os
import sys
import shutil

args = sys.argv[1:]
input_directory = args[0]
output_directory = args[1]
max_depth = None

if "--max_depth" in args:
    max_depth_index = args.index("--max_depth") + 1
    if max_depth_index < len(args):
        max_depth = int(args[max_depth_index])

os.makedirs(output_directory, exist_ok=True)

for curr_dir, folder, name in os.walk(input_directory):
    rel_path = os.path.relpath(curr_dir, input_directory)
    if rel_path == ".":
        path_components = []
    else:
        path_components = rel_path.split(os.sep)

    depth = len(path_components)

    if max_depth is not None and depth > max_depth:
        folder.clear()
        continue

    if max_depth is not None:
        start_index = max(0, depth - max_depth)
        list_of_folders = path_components[start_index:]
    else:
        list_of_folders = path_components

    if list_of_folders:
        short_path = os.path.join(*list_of_folders)
    else:
        short_path = "."
    last_folder = os.path.join(output_directory, short_path)

    os.makedirs(last_folder, exist_ok=True)

    for filename in sorted(name):
        src = os.path.join(curr_dir, filename)
        base, ext = os.path.splitext(filename)
        dst = os.path.join(last_folder, filename)

        counter = 1
        while os.path.exists(dst):
            dst = os.path.join(last_folder, f"{base}_{counter}{ext}")
            counter += 1

        shutil.copy2(src, dst)
