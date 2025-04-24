import os
import sys
import shutil


def do_copy(in_dir, out_dir, max_depth=None):
    if not os.path.isdir(in_dir):
        sys.exit(1)

    os.makedirs(out_dir, exist_ok=True)
    used_names = set()

    for root, dirs, files in os.walk(in_dir):
        dirs.sort()
        files.sort()
        rel_path = os.path.relpath(root, in_dir)
        depth = 0 if rel_path == "." else rel_path.count(os.sep) + 1

        if max_depth is not None and depth >= max_depth:
            dirs[:] = []

        if max_depth is not None and depth > max_depth:
            trimmed = os.sep.join(rel_path.split(os.sep)[:max_depth])
            dst_dir = os.path.join(out_dir, trimmed)
        else:
            dst_dir = os.path.join(out_dir, rel_path)

        os.makedirs(dst_dir, exist_ok=True)

        for f in files:
            src_path = os.path.join(root, f)
            name, ext = os.path.splitext(f)
            dst_path = os.path.join(dst_dir, f)
            count = 1

            while dst_path in used_names or os.path.exists(dst_path):
                dst_path = os.path.join(dst_dir, f"{name}_{count}{ext}")
                count += 1

            used_names.add(dst_path)
            shutil.copy2(src_path, dst_path)


if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    max_depth = None

    if "--max_depth" in sys.argv:
        idx = sys.argv.index("--max_depth")
        max_depth = int(sys.argv[idx + 1])

    do_copy(in_dir, out_dir, max_depth)
