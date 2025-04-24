import os
import sys
import shutil


def do_copy(in_dir, out_dir, max_depth=None):
    if not os.path.exists(in_dir):
        sys.exit(1)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    names = {}
    for curr_root, folders, files in os.walk(in_dir):
        rel_path = os.path.relpath(curr_root, in_dir)
        depth = 0 if rel_path == "." else rel_path.count(os.sep) + 1
        if max_depth is not None and depth > max_depth:
            folders[:] = []
            continue
        for f in files:
            if max_depth is not None and depth > max_depth:
                continue

            orig_path = os.path.join(curr_root, f)

            if f in names:
                names[f] += 1
                dot = f.rfind(".")
                if dot != -1:
                    new_name = f[:dot] + f"_" + str(names[f]) + f[dot:]
                else:
                    new_name = f + "_" + str(names[f])
            else:
                names[f] = 1
                new_name = f

            final_path = os.path.join(out_dir, new_name)
            shutil.copy2(orig_path, final_path)


in_dir = sys.argv[1]
out_dir = sys.argv[2]
max_depth = None
if "--max_depth" in sys.argv:
    idx = sys.argv.index("--max_depth")
    max_depth = int(sys.argv[idx + 1])

do_copy(in_dir, out_dir, max_depth)
