import os
import sys
import shutil

args = sys.argv[1:]
input_directory = args[0]
output_directory = args[1]
max_depth = None

if "--max_depth" in args:
    idx = args.index("--max_depth")
    if idx + 1 < len(args):
        max_depth = int(args[idx + 1])


os.makedirs(output_directory, exist_ok=True)

for curr_dir, folder, name in os.walk(input_directory):
    rel_path = os.path.relpath(curr_dir, input_directory)
    if rel_path == ".":
        path_components = []
    else:
        path_components = rel_path.split(os.sep)

    depth = len(path_components)

    if max_depth is not None and depth > max_depth:
        folder[:] = []
        continue

    if max_depth is not None:
        start_index = max(0, depth - max_depth)
        list_of_folders = path_components[-max_depth:]
    else:
        list_of_folders = path_components

    if list_of_folders:
        short_path = os.path.join(output_directory, *list_of_folders)
    else:
        short_path = output_directory

    os.makedirs(short_path, exist_ok=True)

    for filename in sorted(name):
        src = os.path.join(curr_dir, filename)
        base, ext = os.path.splitext(filename)
        dst = os.path.join(short_path, filename)

        counter = 1
        while os.path.exists(dst):
            dst = os.path.join(short_path, f"{base}_{counter}{ext}")
            counter += 1

        shutil.copy2(src, dst)
