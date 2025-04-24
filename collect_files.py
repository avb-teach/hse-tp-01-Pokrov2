import os
import sys
import shutil


def do_copy(in_dir, out_dir, max_depth=None):

    for root, dirs, files in os.walk(in_dir):
        rel_path = os.path.relpath(root, in_dir)
        depth = 0 if rel_path == "." else rel_path.count(os.sep) + 1

        if max_depth is not None and depth >= max_depth:
            dirs[:] = []

        for f in files:
            src_path = os.path.join(root, f)

            if max_depth is not None and depth >= max_depth:
                limited_path = os.path.join(*rel_path.split(os.sep)[:max_depth])
            else:
                limited_path = rel_path

            dst_dir = os.path.join(out_dir, limited_path)
            os.makedirs(dst_dir, exist_ok=True)

            dst_path = os.path.join(dst_dir, f)
            name, ext = os.path.splitext(f)
            count = 1

            while os.path.exists(dst_path):
                dst_path = os.path.join(dst_dir, f"{name}_{count}{ext}")
                count += 1

            shutil.copy2(src_path, dst_path)


in_dir = sys.argv[1]
out_dir = sys.argv[2]
max_depth = None

if "--max_depth" in sys.argv:
    idx = sys.argv.index("--max_depth")
    max_depth = int(sys.argv[idx + 1])

do_copy(in_dir, out_dir, max_depth)
