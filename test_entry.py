"""Tests for the news-image-20261121 entry.

Run from the repo root:  python3 test_entry.py
Checks the gate rules (PNG, <= 1 MiB, <= 1024x1024), the determinism
rule (two runs of main.py write byte-identical files), the date string
in the layout source, and that main.py makes no network call.
"""

import hashlib
import os
import re
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
NEWS = os.path.join(HERE, "news.png")
MAIN = os.path.join(HERE, "main.py")
RENDER = os.path.join(HERE, "render.py")
LIMIT = 1048576


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(33)
    assert head[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG file"
    assert head[12:16] == b"IHDR", "no IHDR chunk"
    w = int.from_bytes(head[16:20], "big")
    h = int.from_bytes(head[20:24], "big")
    return w, h


class EntryTests(unittest.TestCase):
    def test_image_exists_and_under_size_limit(self):
        self.assertTrue(os.path.exists(NEWS), "news.png missing")
        self.assertLessEqual(os.path.getsize(NEWS), LIMIT,
                            "news.png over the 1 MiB limit")

    def test_image_dimensions_within_1024(self):
        w, h = png_size(NEWS)
        self.assertLessEqual(w, 1024)
        self.assertLessEqual(h, 1024)
        self.assertEqual((w, h), (1024, 1024))

    def test_layout_names_the_day(self):
        with open(RENDER, encoding="utf-8") as f:
            src = f.read()
        self.assertIn("21 November 2026", src)

    def test_main_py_has_no_network_call(self):
        with open(MAIN, encoding="utf-8") as f:
            src = f.read()
        for banned in ("socket", "urllib", "requests", "http.client",
                       "urlopen", "httpx"):
            self.assertNotIn(banned, src, f"main.py mentions {banned}")

    def test_two_runs_are_byte_identical(self):
        hashes = []
        for _ in range(2):
            with tempfile.TemporaryDirectory() as tmp:
                env = dict(os.environ, MAKEFUN_OUTPUT_DIR=tmp)
                r = subprocess.run(
                    [sys.executable, MAIN], cwd=HERE, env=env,
                    capture_output=True, text=True, timeout=60)
                self.assertEqual(r.returncode, 0, r.stderr)
                out = os.path.join(tmp, "entry.png")
                self.assertTrue(os.path.exists(out))
                hashes.append(sha256(out))
        self.assertEqual(hashes[0], hashes[1],
                         "two runs produced different bytes")


if __name__ == "__main__":
    unittest.main(verbosity=2)
