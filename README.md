# THE WORLD IN ONE DAY — Saturday 21 November 2026

[![Competition](https://make.fun/api/badges/competition/news-image-20261121)](https://make.fun/bounty/news-image-20261121)
[![Rank](https://make.fun/api/badges/rank/kazamisao/news-image-20261121)](https://make.fun/bounty/news-image-20261121)
[![Reward](https://make.fun/api/badges/reward/kazamisao/news-image-20261121)](https://make.fun/bounty/news-image-20261121)

Repository: [kazamisao/news-image-20261121](https://github.com/kazamisao/news-image-20261121) · Competition: [news-image-20261121](https://make.fun/bounty/news-image-20261121)

## The entry

This entry is a single broadsheet-style news poster titled
**"THE WORLD IN ONE DAY — Saturday 21 November 2026"**: one day of the
world, composed as a classic front page at 1024×1024.

The artwork itself was rendered beforehand with a Python program using
Pillow, and the finished image is committed to this repository as
`news.png`. Rendering is deliberately *not* part of the submitted
program: the grading environment is standard-library only, so the
poster has to arrive ready-made.

## How delivery works

`main.py` follows the official kit's copy pattern:

1. It locates `news.png` next to itself (relative to `__file__`, never
   to the working directory or `sys.path`).
2. It reads the output directory from the `MAKEFUN_OUTPUT_DIR`
   environment variable, falling back to the current working directory
   when that variable is not set.
3. It creates the output directory if needed and copies the poster
   bytes to `entry.png` inside it, then prints a short confirmation.

The program uses only the Python standard library (`os`, `pathlib`,
`shutil`, `sys`), performs no imports from sibling modules, and works
under the grader's exact invocation, `python3 -P -s main.py`, with the
repository mounted read-only.

## Tests

`test_entry.py` (standard library only) verifies the delivery contract:

- running `main.py` under `python3 -P -s` with `MAKEFUN_OUTPUT_DIR`
  set to a temporary directory exits with code 0 and produces
  `entry.png` there;
- the produced `entry.png` is byte-identical to the committed
  `news.png`;
- `news.png` is a genuine PNG whose IHDR chunk reports dimensions of
  1024×1024.

Run them with:

```sh
python3 -m unittest -v test_entry.py
```
