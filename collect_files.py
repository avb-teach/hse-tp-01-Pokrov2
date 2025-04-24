import os
import sys
import shutil


def do_copy(in_dir, out_dir, max_depth=None):
    if not os.path.exists(in_dir):
        sys.exit(1)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for curr_root, folders, files in os.walk(in_dir):
        rel_path = os.path.relpath(curr_root, in_dir)
        depth = rel_path.count(os.sep)

        if max_depth is not None and depth >= max_depth:
            folders[:] = []

        target_dir = os.path.join(out_dir, rel_path)
        os.makedirs(target_dir, exist_ok=True)

        for f in files:
            src_path = os.path.join(curr_root, f)
            dst_path = os.path.join(target_dir, f)
            shutil.copy2(src_path, dst_path)


in_dir = sys.argv[1]
out_dir = sys.argv[2]
max_depth = None

if "--max_depth" in sys.argv:
    idx = sys.argv.index("--max_depth")
    max_depth = int(sys.argv[idx + 1])

do_copy(in_dir, out_dir, max_depth)
