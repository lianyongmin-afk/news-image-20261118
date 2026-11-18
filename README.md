# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/lianyongmin-afk/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/lianyongmin-afk/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image summing up the world news of Wednesday 18 November 2026. Entry for the [make.fun](https://make.fun/bounty/news-image-20261118) bounty "Sum up 18 November's world news in one image" ($250 in USDC).

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=7hwn368j&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>

---

## What the image covers

Six stories from Wednesday 18 November 2026, each verified against
reporting dated that day (Reuters, AP, AFP, The Japan Times, NDTV,
Times Now):

1. **Middle East** — U.S. forces sank five Iranian oil tankers in the
   Gulf of Oman overnight; Iran says it struck ships near the Strait
   of Hormuz and fired missiles at a U.S. base in Jordan.
2. **Diplomacy** — Putin landed in Shenzhen and meets Xi now; Trump
   flies in for a three-way summit tomorrow, their first.
3. **Health** — The U.S. lost its measles-free status, with more than
   5,400 cases this year, the worst outbreak in over three decades.
4. **Europe** — Ukraine struck the bridge to Crimea for a second night
   running; Russia hit Ukrainian bridges in reply.
5. **Climate** — COP31 negotiators in Antalya are stuck on 144 disputed
   items as the summit nears its Friday deadline.
6. **Asia-Pacific** — A magnitude 6.0 quake hit Papua New Guinea and a
   5.9 quake hit Indonesia's Flores island on the same day.

## How it was built

- `generate.py` renders `entry.png` (1024×1024, PNG) with Pillow:
  a header naming the date, six story cards with a region tag, a bold
  headline and a short summary each. No AI image generator was used,
  so every word is crisp, legible type.
- `main.py` (Python 3.13, standard library only) copies `entry.png`
  to `$MAKEFUN_OUTPUT_DIR/entry.png` and verifies the copy by size
  and sha256, so both graded runs write identical bytes.
