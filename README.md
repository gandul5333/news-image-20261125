# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/gandul5333/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/gandul5333/news-image-20261125/reward.svg)](https://github.com/gandul5333/news-image-20261125)

The world in one day: a newspaper-style poster summing up Wednesday 25 November 2026. The lead story is two oil tankers striking naval mines and catching fire in the Strait of Hormuz, with Yemen's Houthis saying they also hit Saudi Arabia's Ras Tanura refinery. Around it: Asian and US stocks sinking as Washington proposes new tariffs on 14 trading partners, Huawei convicted by a Brooklyn jury on 10 of 12 counts, Ukrainian drones setting two Rosneft refineries ablaze, Shenzhou-24 carrying Pakistan's first astronaut to China's Tiangong station, Australia signing a security treaty with Solomon Islands, and RSF drone strikes killing 19 civilians in Sudan — plus the day in brief in the footer ticker. The image is drawn entirely in code by `draw_image.py` (Pillow + DejaVu fonts, no photographs, no network); `main.py` (Python 3.13, standard library only) copies it to the output and verifies its SHA-256.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Regenerate the poster

```sh
python3 draw_image.py
```
