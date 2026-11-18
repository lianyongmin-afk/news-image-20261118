#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261118.

Copies the pre-rendered infographic entry.png (which sits beside this
file in the repository) to $MAKEFUN_OUTPUT_DIR/entry.png, creating the
output directory if needed. Standard library only, no network, and
fully deterministic: the output is a byte-for-byte copy of entry.png,
verified by comparing the written file's size and sha256 against the
source before exiting.
"""

import hashlib
import os
import sys


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print(f"error: {src} not found", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")

    with open(src, "rb") as fh:
        data = fh.read()
    with open(dst, "wb") as fh:
        fh.write(data)

    # verify the copy is exact, so both graded runs produce identical bytes
    if os.path.getsize(dst) != len(data) or sha256_of(dst) != hashlib.sha256(data).hexdigest():
        print(f"error: verification failed for {dst}", file=sys.stderr)
        return 1

    print(f"wrote {dst} ({len(data)} bytes, sha256 {hashlib.sha256(data).hexdigest()[:16]}...)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
