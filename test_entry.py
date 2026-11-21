"""Tests for the news-image entry delivery program.

These tests use only the Python standard library. They check the
exact contract the grader relies on:

- main.py runs cleanly under ``python3 -P -s`` with
  MAKEFUN_OUTPUT_DIR pointing at a fresh directory;
- the file it produces is byte-identical to the committed poster;
- the committed poster really is a 1024x1024 PNG.
"""

import os
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent
MAIN_PY = REPO_DIR / "main.py"
POSTER = REPO_DIR / "news.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def run_main(output_dir: Path) -> subprocess.CompletedProcess:
    """Run main.py exactly the way the grader does."""
    env = dict(os.environ)
    env["MAKEFUN_OUTPUT_DIR"] = str(output_dir)
    return subprocess.run(
        [sys.executable, "-P", "-s", str(MAIN_PY)],
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )


class TestGraderRun(unittest.TestCase):
    def test_main_exits_zero_and_writes_entry_png(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "out"
            result = run_main(output_dir)
            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout={result.stdout!r} stderr={result.stderr!r}",
            )
            self.assertTrue(
                (output_dir / "entry.png").is_file(),
                "entry.png was not created in MAKEFUN_OUTPUT_DIR",
            )

    def test_entry_png_matches_committed_poster_byte_for_byte(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "out"
            result = run_main(output_dir)
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            produced = (output_dir / "entry.png").read_bytes()
            expected = POSTER.read_bytes()
            self.assertEqual(produced, expected)


class TestPosterImage(unittest.TestCase):
    def test_poster_is_png_with_expected_dimensions(self):
        data = POSTER.read_bytes()
        self.assertTrue(
            data.startswith(PNG_SIGNATURE), "news.png lacks the PNG signature"
        )
        # The IHDR chunk follows the 8-byte signature: 4 bytes of chunk
        # length, the 4-byte type "IHDR", then width and height as
        # big-endian uint32 values.
        self.assertEqual(data[12:16], b"IHDR")
        width, height = struct.unpack(">II", data[16:24])
        self.assertEqual((width, height), (1024, 1024))


if __name__ == "__main__":
    unittest.main(verbosity=2)
