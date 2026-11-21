# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/kazamisao/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/kazamisao/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A one-page broadsheet of the world news of Saturday, 21 November 2026, drawn in code with Pillow: NATO chief Mark Rutte flying to Warsaw as the hero story, after Russian missiles fell on Polish soil on Friday and Warsaw called it a deliberate provocation, Friday's Wall Street rout and the Shenzhen summit's thin result beside it, plus the Saudi–Houthi exchange, the daraxonrasib cancer-pill trial, COP31 and the Palisades fire verdict — with an "Also today" strip on Estonia's border closure, Austria summoning Russia's envoy, the Kryvyi Rih strike, and gold and Bitcoin sliding. `render.py` draws the image at 3x and downscales it to `news.png`; `main.py` (stdlib only) copies it to the output path, byte-identical on every run.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Tests

```sh
python3 test_entry.py
```

The suite checks the gate rules: `news.png` is a valid PNG of 1024x1024 and under 1 MiB, and two runs of `main.py` write byte-identical files.

---

<sub>Entered on [make.fun](https://make.fun/?ref=p5dwa49p&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
