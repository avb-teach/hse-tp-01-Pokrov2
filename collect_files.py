import os
import sys
import shutil


def do_copy(in_dir, out_dir, max_depth=None):
    if not os.path.exists(in_dir):
        sys.exit(1)
    os.makedirs(out_dir, exist_ok=True)

    seen = {}

    for root, dirs, files in os.walk(in_dir):
        rel = os.path.relpath(root, in_dir)
        depth = 0 if rel == "." else rel.count(os.sep) + 1

        if max_depth is not None and depth >= max_depth:
            dirs[:] = []

        dest_dir = os.path.join(out_dir, rel) if rel != "." else out_dir
        os.makedirs(dest_dir, exist_ok=True)

        for f in sorted(files):
            if max_depth is not None and depth > max_depth:
                continue

            src = os.path.join(root, f)
            dst = os.path.join(dest_dir, f)

            base, ext = os.path.splitext(f)
            suffix = 1

            while os.path.exists(dst):
                dst = os.path.join(dest_dir, f"{base}_{suffix}{ext}")
                suffix += 1

            shutil.copy2(src, dst)


in_dir = sys.argv[1]
out_dir = sys.argv[2]
max_depth = None
if "--max_depth" in sys.argv:
    i = sys.argv.index("--max_depth")
    max_depth = int(sys.argv[i + 1])

do_copy(in_dir, out_dir, max_depth)
