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

        if max_depth is not None and depth >= max_depth:
            dirs[:] = []

        target_dirs = []

        if max_depth is None or depth <= max_depth:
            target_dirs.append(os.path.join(out_dir, rel_path))

        if max_depth is not None and depth > max_depth:
            parts = rel_path.split(os.sep)
            trimmed = os.sep.join(parts[:max_depth])
            target_dirs.append(os.path.join(out_dir, trimmed))

        for target in target_dirs:
            os.makedirs(target, exist_ok=True)

        for name in files:
            src = os.path.join(root, name)

            for target in target_dirs:
                dst = os.path.join(target, name)
                base, ext = os.path.splitext(name)
                i = 1
                while os.path.exists(dst):
                    dst = os.path.join(target, f"{base}_{i}{ext}")
                    i += 1
                shutil.copy2(src, dst)


in_dir = sys.argv[1]
out_dir = sys.argv[2]
max_depth = None

if "--max_depth" in sys.argv:
    idx = sys.argv.index("--max_depth")
    max_depth = int(sys.argv[idx + 1])

do_copy(in_dir, out_dir, max_depth)
