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
        dirs.sort()
        files.sort()
        if rel_path == ".":
            depth = 0
        else:
            rel_path.count(os.sep) + 1

        if max_depth is not None and depth > max_depth:
            dirs[:] = []
            continue

        dst_dir = os.path.join(out_dir, rel_path)
        os.makedirs(dst_dir, exist_ok=True)

        for name in files:
            src_path = os.path.join(root, name)

            key = name
            if key in names:
                names[key] += 1
                count = names[key] - 1
                dot = name.rfind(".")
                if dot != -1:
                    new_name = name[:dot] + "_" + str(count) + name[dot:]
                else:
                    new_name = name + "_" + str(count)
            else:
                names[key] = 1
                new_name = name

            dst_path = os.path.join(dst_dir, new_name)
            shutil.copy2(src_path, dst_path)


in_dir = sys.argv[1]
out_dir = sys.argv[2]
max_depth = None
if "--max_depth" in sys.argv:
    i = sys.argv.index("--max_depth")
    max_depth = int(sys.argv[i + 1])

do_copy(in_dir, out_dir, max_depth)
