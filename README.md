# bountyhawk-news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/raditsaputra4004-prog/bountyhawk-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/raditsaputra4004-prog/bountyhawk-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

World News — Friday 20 November 2026. One image summing up the day's world news, drawn entirely in code: Russia's overnight missile raids on Kyiv's Dnipro bridges; the Houthis claiming four new strikes on Saudi targets; 13,000 marching in Tokyo against the Takaichi government; Japan's core inflation hitting a 2026 high at 2.2%; Trump's posthumous pardon of Pete Rose; and the WHO keeping the DR Congo Ebola outbreak an international emergency — plus a ticker of the day's other stories.

`tools/draw.py` draws `entry.png` (1024×1024) with Pillow and DejaVu fonts. `main.ts` copies it to the output directory, byte for byte, every run.

## Run it

```sh
python3 tools/draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=2yq7mcmp&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
