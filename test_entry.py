"""Tests for the news-image-20261121 entry.

Covers: output existence, PNG validity and exact size,
byte-identical re-rendering, and presence of key headlines
in the source files.
"""

import hashlib
import os
import subprocess
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PNG_PATH = os.path.join(HERE, "news.png")


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _run_main():
    result = subprocess.run(
        [sys.executable, os.path.join(HERE, "main.py")],
        cwd=HERE, capture_output=True, text=True, timeout=120,
    )
    assert result.returncode == 0, f"main.py failed: {result.stderr}"


def test_output_exists_after_run():
    _run_main()
    assert os.path.isfile(PNG_PATH), "news.png was not created"


def test_png_valid_and_exact_size():
    if not os.path.isfile(PNG_PATH):
        _run_main()
    with Image.open(PNG_PATH) as img:
        assert img.format == "PNG"
        assert img.size == (1024, 1024), f"unexpected size {img.size}"


def test_rerender_is_byte_identical():
    _run_main()
    first = _sha256(PNG_PATH)
    _run_main()
    second = _sha256(PNG_PATH)
    assert first == second, "re-render produced different bytes"


def test_key_headlines_in_sources():
    combined = ""
    for name in ("main.py", "render.py", "README.md"):
        with open(os.path.join(HERE, name), encoding="utf-8") as fh:
            combined += fh.read() + "\n"
    for needle in (
        "THE WORLD IN ONE DAY",
        "SATURDAY 21 NOVEMBER 2026",
        "Poland",
        "Rutte",
        "Warsaw",
        "Nasdaq",
        "Nvidia",
        "Shenzhen",
        "COP31",
        "Palisades",
        "daraxonrasib",
    ):
        assert needle in combined, f"missing headline string: {needle}"


if __name__ == "__main__":
    test_output_exists_after_run()
    print("PASS test_output_exists_after_run")
    test_png_valid_and_exact_size()
    print("PASS test_png_valid_and_exact_size")
    test_rerender_is_byte_identical()
    print("PASS test_rerender_is_byte_identical")
    test_key_headlines_in_sources()
    print("PASS test_key_headlines_in_sources")
    print("All 4 tests passed.")
