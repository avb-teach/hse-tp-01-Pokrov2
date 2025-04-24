import os
import sys
import shutil

def do_copy(in_dir, out_dir, max_depth=None):
    if not os.path.exists(in_dir):
        sys.exit(1)
    os.makedirs(out_dir, exist_ok=True)

    names = {}

    for root, dirs, files in os.walk(in_dir):
        rel_path = os.path.relpath(root, in_dir)
        depth = 0 if rel_path == "." else rel_path.count(os.sep) + 1

        if max_depth is not None and depth > max_depth:
            dirs[:] = []
            continue

        for name in files:
            full_path = os.path.join(root, name)

            if name in names:
                names[name] += 1
                dot = name.rfind(".")
                if dot != -1:
                    new_name = name[:dot] + "_" + str(names[name]) + name[dot:]
                else:
                    new_name = name + "_" + str(names[name])
            else:
                names[name] = 1
                new_name = name

            dst_path = os.path.join(out_dir, new_name)
            shutil.copy(full_path, dst_path)

in_dir = sys.argv[1]
out_dir = sys.argv[2]
max_depth = None

if "--max_depth" in sys.argv:
    i = sys.argv.index("--max_depth")
    max_depth = int(sys.argv[i + 1])

do_copy(in_dir, out_dir, max_depth)
