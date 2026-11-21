# The World in One Day — news-image-20261121

[![Competition](https://make.fun/api/badges/competition/news-image-20261121)](https://make.fun/competitions/news-image-20261121)
[![Rank](https://make.fun/api/badges/competition/news-image-20261121/repo/kazamisao/news-image-20261121/rank)](https://make.fun/competitions/news-image-20261121)
[![Reward](https://make.fun/api/badges/competition/news-image-20261121/repo/kazamisao/news-image-20261121/reward)](https://make.fun/competitions/news-image-20261121)

A single Python program that prints a whole day of news onto one page.

Run it and you get `news.png`: a 1024 by 1024 broadsheet poster in a
classic newspaper style — a large serif masthead reading
"THE WORLD IN ONE DAY", a dateline for SATURDAY 21 NOVEMBER 2026,
black ink on off-white paper, ruled lines between sections, and a
clear ladder of headline sizes from the lead story down to the briefs.

## What is on the page

The lead story covers the Russian missile that struck Poland on
Friday and the visit by NATO Secretary General Rutte to Warsaw
today, laid out across two columns under the main headline.

Below it, the markets story reports a rough day for investors:
Wall Street down 3,7%, the Nasdaq down 5,3%, and Nvidia down 14%,
with the headline figures repeated in a small boxed strip so a
reader can take them in at a glance.

The lower half carries five shorter items in two columns:
Shenzhen and its latest technology push, renewed Saudi–Houthi
tensions, the daraxonrasib cancer-drug news, the COP31 climate
summit, and the Palisades fire recovery.

## How it works

- `main.py` is the entrypoint. Running `python3 main.py` writes
  `news.png` next to the script.
- `render.py` holds all of the drawing code: canvas, fonts, text
  wrapping, column layout, rules and the figures box.
- `test_entry.py` checks that the output exists, that it is a
  valid PNG of exactly 1024x1024, that rendering twice gives the
  same bytes, and that the key headlines are present in the sources.

## Determinism

There is no randomness here and nothing reads the clock. Every
string, coordinate and colour is fixed in the source, so running
the program twice produces a byte-identical `news.png`. That makes
the poster easy to verify: regenerate it, compare the hash, and
the page either matches or it does not.

## Requirements

Python 3 with Pillow. No network access is needed at runtime.
