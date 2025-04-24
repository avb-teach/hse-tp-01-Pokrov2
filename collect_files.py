import os
import sys
import shutil


def do_copy(in_dir, out_dir, max_depth=None):
    if not os.path.isdir(in_dir):
        sys.exit(1)

    os.makedirs(out_dir, exist_ok=True)
    used_names = {}

    for root, dirs, files in os.walk(in_dir):
        rel_path = os.path.relpath(root, in_dir)
        depth = 0 if rel_path == "." else rel_path.count(os.sep) + 1

        if max_depth is not None and depth >= max_depth:
            dirs[:] = []

        for file in sorted(files):
            src_path = os.path.join(root, file)

            if max_depth is not None and depth > max_depth:
                rel_parts = rel_path.split(os.sep)
                trimmed = os.path.join(*rel_parts[:max_depth])
                dst_dir = os.path.join(out_dir, trimmed)
            else:
                dst_dir = os.path.join(out_dir, rel_path)

            os.makedirs(dst_dir, exist_ok=True)

            base, ext = os.path.splitext(file)
            dst_path = os.path.join(dst_dir, file)
            count = 1

            while os.path.exists(dst_path):
                dst_path = os.path.join(dst_dir, f"{base}_{count}{ext}")
                count += 1

            shutil.copy2(src_path, dst_path)


in_dir = sys.argv[1]
out_dir = sys.argv[2]
max_depth = None

if "--max_depth" in sys.argv:
    idx = sys.argv.index("--max_depth")
    max_depth = int(sys.argv[idx + 1])

do_copy(in_dir, out_dir, max_depth)
