"""Entry program for news-image-20261121 (stdlib only).

The picture itself sits next to this file as news.png: a one-page
broadsheet of the world news of Saturday, 21 November 2026, drawn by
render.py (Pillow, run at build time) -- NATO chief Mark Rutte flying
to Warsaw after Russian missiles fell on Polish soil, Friday's Wall
Street rout and the Shenzhen summit beside it, plus the Saudi-Houthi
exchange, the daraxonrasib cancer-pill trial, COP31 and the Palisades
fire verdict, with an "Also today" strip. Entries close Monday
23 November 2026, 00:00 UTC.

All this program does is deliver those bytes, untouched, to the output
path the harness expects. It runs with no network and writes the same
bytes on every run.
"""

import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "news.png")
LIMIT = 1048576


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(out_dir, "entry.png")


def main():
    # The gate rejects anything over 1 MiB, so fail loudly if the bundled
    # picture ever grows past the cap instead of writing a bad entry.
    if os.path.getsize(SOURCE) > LIMIT:
        raise SystemExit("news.png exceeds the 1 MiB entry limit")
    out = output_path()
    os.makedirs(os.path.dirname(out), exist_ok=True)
    shutil.copyfile(SOURCE, out)
    print(f"wrote {out} sha256={sha256(out)}")


if __name__ == "__main__":
    main()
