# makefun-news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/yuseisako222-arch/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/yuseisako222-arch/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A Node 22 program that publishes one newspaper-style front page summing up the world news of Friday 20 November 2026 — the ICJ's Myanmar genocide ruling, the first Trump–Xi–Putin summit in Shenzhen, the Russian barrage on Kyiv, the global AI stock sell-off and more — as a single 1024x1024 PNG written to /output/entry.png. The image is drawn deterministically by build_image.py (Pillow) and committed as entry.png; main.ts copies it to the output directory.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=9vf7ext6&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
