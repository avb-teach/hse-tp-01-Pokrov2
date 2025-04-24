import os
import sys
import shutil


def do_copy(in_dir, out_dir, max_depth=None):
    if not os.path.isdir(in_dir):
        sys.exit("No input directory")

    os.makedirs(out_dir, exist_ok=True)
    used_names = {}
    for root, dirs, files in os.walk(in_dir):
        rel = os.path.relpath(root, in_dir)
        depth = 0 if rel == "." else rel.count(os.sep) + 1
        if max_depth is not None and depth >= max_depth:
            dirs[:] = []

        targets = []

        if max_depth is None or depth <= max_depth:
            targets.append(os.path.join(out_dir, rel))

        if max_depth is not None and depth > max_depth:
            limited_parts = rel.split(os.sep)[:max_depth]
            limited_path = os.path.join(out_dir, *limited_parts)
            targets.append(limited_path)

        for tdir in targets:
            os.makedirs(tdir, exist_ok=True)

        for file in files:
            src_path = os.path.join(root, file)

            for tdir in targets:
                dst_path = os.path.join(tdir, file)
                name, ext = os.path.splitext(file)
                count = 1
                while dst_path in used_names.values() or os.path.exists(dst_path):
                    dst_path = os.path.join(tdir, f"{name}_{count}{ext}")
                    count += 1
                used_names[(tdir, file)] = dst_path
                shutil.copy2(src_path, dst_path)


if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    max_depth = None

    if "--max_depth" in sys.argv:
        idx = sys.argv.index("--max_depth")
        max_depth = int(sys.argv[idx + 1])

    do_copy(in_dir, out_dir, max_depth)
