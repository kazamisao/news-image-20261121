"""Entrypoint for the news-image-20261121 entry.

Running this file produces news.png next to this script:
a deterministic one-page broadsheet poster at 1024x1024.
The output path is anchored to this file's folder so the
result lands in the repo root no matter where it is run from.
"""

import os

from render import render

OUTPUT_NAME = "news.png"
EXPECTED_SIZE = (1024, 1024)


def output_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, OUTPUT_NAME)


def main():
    target = output_path()
    render(target)
    # Lightweight sanity note for anyone running it by hand.
    size = os.path.getsize(target)
    print(f"Wrote {target} ({size} bytes, expected canvas {EXPECTED_SIZE[0]}x{EXPECTED_SIZE[1]})")


if __name__ == "__main__":
    main()
