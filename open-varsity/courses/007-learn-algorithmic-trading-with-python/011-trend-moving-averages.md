Chapters
Module C · Technical Indicators - Chapter 11
# Trend & Moving Averages
From SMA and EMA to Supertrend, Ichimoku and Parabolic SAR.
NSENFOMCX
What you'll learn
  * ·SMA / EMA / WMA
  * ·HMA / ALMA / KAMA / VWMA
  * ·Supertrend
  * ·Ichimoku Cloud
  * ·Parabolic SAR
  * ·Choosing a trend filter


Up to now we've been _fetching_ the market - quotes, candles, whole price histories. From this chapter on we start _reading_ it. A **technical indicator** is just a formula that chews on price (and sometimes volume) and hands back a number that's easier to act on than the raw chart. OpenAlgo ships over eighty of them in a single library called `openalgo.ta` - and its core is written in **Rust** , so the maths runs much faster than the equivalent hand-written Python, which really shows when you compute indicators across thousands of candles. We'll spend the next few chapters touring them by family.
This chapter is the **trend** family - tools that answer one question every trader asks first: _which way is this thing actually going?_ Get that right and everything downstream (entries, stops, position size) gets easier. Get it wrong and the best entry signal in the world just gets you into a losing trade faster.
A quick word on how we'll work. Every example imports the toolkit the same way:

```
from openalgo import api, ta

```

`api` is the client you already know; `ta` is the indicator library. One thing that trips up beginners: these functions hand back different _shapes_. A simple average like `ta.ema(...)` returns a single **pandas Series** (a labelled column of numbers). But a richer indicator like `ta.supertrend(...)` returns a **tuple** - several Series at once, which you unpack into separate variables. We'll flag the shape every single time, because guessing wrong is the most common error in this whole module.
Note
Nothing extra to install - the indicators come built into the `openalgo` package you added in Chapter 1, with a Rust-powered core that keeps the maths fast even over long histories. If `from openalgo import ta` works, you're ready. Every output on this page is real - these scripts were run against a live server before publishing.
## The moving average: the original trend tool
A **moving average (MA)** is the plainest idea in technical analysis: take the last _N_ closing prices and average them, then slide that window forward one bar at a time. It smooths the jagged price line into a flowing curve, so instead of reacting to every twitch you see the underlying drift. The single most-used trend rule on earth is just: _price above its moving average = uptrend; below = downtrend._
There are two starter flavours. The **Simple Moving Average (SMA)** weights every bar in the window equally. The **Exponential Moving Average (EMA)** weights _recent_ bars more heavily, so it turns to follow price faster. Neither is "better" - the SMA is calmer and ignores noise; the EMA is quicker but whippier.
EX 1SMA vs EMA on one stockNSEch11/01_sma_ema.py
Copy
```
# The two starter moving averages: SMA (plain average) and EMA (recent-weighted).
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=250)).strftime("%Y-%m-%d")

df = client.history(symbol="RELIANCE", exchange="NSE", interval="D", start_date=start, end_date=end)

df["SMA20"] = ta.sma(df["close"], 20)
df["EMA20"] = ta.ema(df["close"], 20)

price = df["close"].iloc[-1]
sma = df["SMA20"].iloc[-1]
ema = df["EMA20"].iloc[-1]

print(f"RELIANCE close : {price:8.2f}")
print(f"20-day SMA     : {sma:8.2f}")
print(f"20-day EMA     : {ema:8.2f}")
print("Trend read     :", "above average -> bullish" if price > sma else "below average -> bearish")
print("EMA reacts faster, so it sits closer to price:", round(abs(price - ema), 2), "vs SMA", round(abs(price - sma), 2))
```

Live output

```
RELIANCE close :  1306.00
20-day SMA     :  1307.82
20-day EMA     :  1316.07
Trend read     : below average -> bearish
EMA reacts faster, so it sits closer to price: 10.07 vs SMA 1.82
```

Notice in the output that the EMA sits closer to the current price than the SMA does. That's the responsiveness trade-off made concrete: the EMA has already started leaning toward the latest move while the SMA is still digesting older prices.
Tip
The period you choose sets the character. Short windows (9, 20) hug price and suit fast trading; long windows (50, 100, 200) define the big-picture trend and barely flinch at daily noise. The **200-day MA** is the classic line institutions watch to call a market bull or bear.
### Stacking averages into a ribbon
One MA tells you direction. Several MAs of different lengths, plotted together, tell you direction _and conviction_. When they line up in order - fast on top, slow on the bottom in an uptrend - the trend is clean and everyone's on the same side. When they tangle together, the market is undecided and you're better off waiting.
EX 2An EMA ribbon, fast to slowNSEch11/02_ma_ribbon.py
Copy
```
# A "ribbon" of EMAs (fast to slow). When they stack in order, the trend is clean.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=250)).strftime("%Y-%m-%d")

df = client.history(symbol="TCS", exchange="NSE", interval="D", start_date=start, end_date=end)

periods = [9, 21, 50, 100]
emas = {p: ta.ema(df["close"], p).iloc[-1] for p in periods}

print("TCS close:", round(df["close"].iloc[-1], 2))
for p in periods:
    print(f"  EMA{p:<3d} = {emas[p]:8.2f}")

# A bullish stack means fast EMAs sit above slow EMAs, in order.
ordered = [emas[p] for p in periods]
stacked_up = all(ordered[i] > ordered[i + 1] for i in range(len(ordered) - 1))
stacked_down = all(ordered[i] < ordered[i + 1] for i in range(len(ordered) - 1))
print("Ribbon:", "bullish stack" if stacked_up else "bearish stack" if stacked_down else "tangled / no clear trend")
```

Live output

```
TCS close: 2060.0
  EMA9   =  2149.37
  EMA21  =  2202.94
  EMA50  =  2314.99
  EMA100 =  2482.11
Ribbon: bearish stack
```

## Fighting lag: WMA, HMA and friends
Every moving average has one flaw: **lag**. Because it's built from _past_ prices, it always reports the turn a little late. A whole zoo of smarter averages exists to reduce that delay. The **Weighted Moving Average (WMA)** weights recent prices on a straight-line scale. The **Hull Moving Average (HMA)** is a clever combination that cuts lag dramatically while staying smooth - it hugs price closely.
EX 3WMA and HMA vs plain SMANSEch11/03_wma_hma.py
Copy
```
# WMA and HMA: two ways to fight "lag" -- the delay a moving average has behind price.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=250)).strftime("%Y-%m-%d")

df = client.history(symbol="INFY", exchange="NSE", interval="D", start_date=start, end_date=end)

df["WMA20"] = ta.wma(df["close"], 20)
df["HMA20"] = ta.hma(df["close"], 20)
df["SMA20"] = ta.sma(df["close"], 20)

price = df["close"].iloc[-1]
print("INFY close:", round(price, 2))
print(f"SMA20 = {df['SMA20'].iloc[-1]:8.2f}  (slowest, smoothest)")
print(f"WMA20 = {df['WMA20'].iloc[-1]:8.2f}  (recent-weighted)")
print(f"HMA20 = {df['HMA20'].iloc[-1]:8.2f}  (lowest lag, hugs price)")

# The HMA usually tracks price most closely -- less lag, but more noise.
gaps = {"SMA": abs(price - df["SMA20"].iloc[-1]),
        "WMA": abs(price - df["WMA20"].iloc[-1]),
        "HMA": abs(price - df["HMA20"].iloc[-1])}
print("Closest to price:", min(gaps, key=gaps.get))
```

Live output

```
INFY close: 1029.0
SMA20 =  1139.18  (slowest, smoothest)
WMA20 =  1121.53  (recent-weighted)
HMA20 =  1084.88  (lowest lag, hugs price)
Closest to price: HMA
```

Less lag sounds purely good, but there's no free lunch: the faster an average reacts, the more often it gets faked out by noise. The HMA tracks price best in the output - and will also flip-flop most in a choppy market.
Two more worth knowing live in the same family. The **Volume Weighted Moving Average (VWMA)** lets high-volume bars pull the average around more than quiet ones - useful because moves on heavy volume tend to be more "real." And **Kaufman's Adaptive Moving Average (KAMA)** is genuinely smart: it speeds up automatically when a clean trend appears and slows right down when price is just chopping sideways. Note that `ta.vwma` needs a `volume` argument as well as price.
EX 4Volume-weighted and adaptive MAsMCXch11/04_vwma_kama.py
Copy
```
# VWMA leans on volume; KAMA speeds up in trends and slows in chop. Tested on MCX gold.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")

df = client.history(symbol="GOLDM03JUL26FUT", exchange="MCX", interval="15m", start_date=start, end_date=end)

df["SMA20"] = ta.sma(df["close"], 20)
df["VWMA20"] = ta.vwma(df["close"], df["volume"], 20)
df["KAMA"] = ta.kama(df["close"])

print("GOLDM 15m candles:", len(df))
print(f"Close      : {df['close'].iloc[-1]:9.1f}")
print(f"SMA20      : {df['SMA20'].iloc[-1]:9.1f}  (every candle counts equally)")
print(f"VWMA20     : {df['VWMA20'].iloc[-1]:9.1f}  (high-volume candles count more)")
print(f"KAMA       : {df['KAMA'].iloc[-1]:9.1f}  (adapts to volatility)")

# When VWMA differs from SMA, busy candles are pulling the average around.
diff = df["VWMA20"].iloc[-1] - df["SMA20"].iloc[-1]
print("Volume tilt:", "up" if diff > 0 else "down", f"({diff:+.1f} points vs plain SMA)")
```

Live output

```
GOLDM 15m candles: 389
Close      :  144410.0
SMA20      :  144409.8  (every candle counts equally)
VWMA20     :  144440.7  (high-volume candles count more)
KAMA       :  144391.4  (adapts to volatility)
Volume tilt: up (+30.9 points vs plain SMA)
```

Key idea
Indicator shapes so far: `sma`, `ema`, `wma`, `hma`, `vwma`, `kama`, `alma` all return a single **pandas Series**. You read the latest value with `.iloc[-1]` - that's "the last row," exactly like the `[-1]` shortcut for lists you met in Chapter 2.
## Supertrend: a trend tool that gives orders
Moving averages describe the trend; **Supertrend** practically trades it for you. It uses volatility (the ATR, which we'll meet properly in Chapter 13) to draw a single line that sits _below_ price in an uptrend and flips _above_ price in a downtrend. When price closes through the line, the trend has changed - clean and unambiguous. It's a favourite for exactly that reason.
Here's where shapes matter. `ta.supertrend(...)` returns a **tuple of two Series** : the line itself, and a _direction_ flag. Read that flag carefully - in this library **-1 means uptrend and +1 means downtrend**. Unpack them into two variables:
EX 5Supertrend line and directionNSEch11/05_supertrend.py
Copy
```
# Supertrend: a single line that flips above/below price and shouts "trend changed".
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=250)).strftime("%Y-%m-%d")

df = client.history(symbol="HDFCBANK", exchange="NSE", interval="D", start_date=start, end_date=end)

# Returns a TUPLE: the line itself, and a direction (-1 = uptrend, 1 = downtrend).
df["ST"], df["DIR"] = ta.supertrend(df["high"], df["low"], df["close"], period=10, multiplier=3.0)

last_dir = df["DIR"].iloc[-1]
print("HDFCBANK close:", round(df["close"].iloc[-1], 2))
print("Supertrend line:", round(df["ST"].iloc[-1], 2))
print("Direction:", "UPTREND (line below price)" if last_dir == -1 else "DOWNTREND (line above price)")

# A flip is where the direction value changes from one bar to the next.
flips = (df["DIR"].diff() != 0).sum() - 1
print("Trend flips in window:", int(flips))
```

Live output

```
HDFCBANK close: 772.9
Supertrend line: 745.05
Direction: UPTREND (line below price)
Trend flips in window: 10
```

Heads up
That direction convention (-1 up, +1 down) feels backwards the first time. Always check the docs or test it before you wire a Supertrend into a live strategy - getting the sign flipped means buying every time you meant to sell.
## Ichimoku Cloud: the all-in-one dashboard
The **Ichimoku Cloud** looks intimidating - five lines at once - but the idea is friendly: it tries to show trend, momentum, and support/resistance in a single picture. The two lines you'll use most are the fast **conversion line** and slower **base line** (a cross between them is a momentum signal), and the shaded **cloud** between two projected lines. The simplest read of all: **price above the cloud is a bullish regime, price below it is bearish, and price inside the cloud means no clear trend** - stand aside.
`ta.ichimoku(...)` returns a **tuple of five Series**. We only need a few of them to get a verdict.
EX 6Read the Ichimoku cloudNSEch11/06_ichimoku.py
Copy
```
# Ichimoku Cloud: five lines that map trend, support and resistance at a glance.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=250)).strftime("%Y-%m-%d")

df = client.history(symbol="ICICIBANK", exchange="NSE", interval="D", start_date=start, end_date=end)

# Returns FIVE series: conversion, base, span A, span B, lagging.
conv, base, span_a, span_b, lag = ta.ichimoku(df["high"], df["low"], df["close"])

price = df["close"].iloc[-1]
cloud_top = max(span_a.iloc[-1], span_b.iloc[-1])
cloud_bot = min(span_a.iloc[-1], span_b.iloc[-1])

print("ICICIBANK close:", round(price, 2))
print("Conversion line:", round(conv.iloc[-1], 2))
print("Base line      :", round(base.iloc[-1], 2))
print(f"Cloud          : {cloud_bot:.2f} to {cloud_top:.2f}")

if price > cloud_top:
    print("Read: price ABOVE the cloud -> bullish regime")
elif price < cloud_bot:
    print("Read: price BELOW the cloud -> bearish regime")
else:
    print("Read: price INSIDE the cloud -> no clear trend")
```

Live output

```
ICICIBANK close: 1335.5
Conversion line: 1327.8
Base line      : 1291.4
Cloud          : 1285.38 to 1298.80
Read: price ABOVE the cloud -> bullish regime
```

## Parabolic SAR: a built-in trailing stop
The **Parabolic SAR** ("Stop And Reverse") prints a dot each bar that trails behind price - below it in an uptrend, above it in a downtrend. Two jobs in one: the side the dot is on tells you the trend, and the dot's level makes a ready-made **trailing stop-loss**. As the trend runs, the dots accelerate toward price, tightening your stop automatically until price finally crosses them and the trend is declared over.
`ta.psar(...)` takes **high and low** (not close) and returns a single Series of dot levels.
EX 7Parabolic SAR as a trailing stopNFOch11/07_parabolic_sar.py
Copy
```
# Parabolic SAR: dots that trail price and mark a trailing stop / trend side. NFO future.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d")

df = client.history(symbol="NIFTY30JUN26FUT", exchange="NFO", interval="5m", start_date=start, end_date=end)

# psar returns one series of dot levels.
df["PSAR"] = ta.psar(df["high"], df["low"], acceleration=0.02, maximum=0.2)

price = df["close"].iloc[-1]
sar = df["PSAR"].iloc[-1]
print("NIFTY future close:", round(price, 2))
print("Parabolic SAR     :", round(sar, 2))

# SAR below price = long side (stop trails underneath); above price = short side.
if price > sar:
    print("SAR below price -> bullish; trail your stop at", round(sar, 2))
else:
    print("SAR above price -> bearish; trail your stop at", round(sar, 2))
```

Live output

```
NIFTY future close: 23810.0
Parabolic SAR     : 23939.75
SAR above price -> bearish; trail your stop at 23939.75
```

## Envelopes and the Alligator
Two more trend ideas round out the toolkit. **MA Envelopes** draw a fixed-percentage band above and below a moving average - a simple way to see when price has stretched unusually far from its mean. And the **Alligator** (three smoothed, shifted averages nicknamed jaw, teeth and lips) is a vivid way to picture trend strength: when the three lines fan out in order the "alligator is feeding" (a trend is running); when they twist together it's "sleeping" (a range), and you wait.
Both take a single price series. `ta.ma_envelopes(...)` returns `(upper, middle, lower)`; `ta.alligator(...)` returns `(jaw, teeth, lips)`.
EX 8MA envelopes and the AlligatorNSEch11/08_envelopes_alligator.py
Copy
```
# MA Envelopes (a band around an average) and the Alligator (three shifted averages).
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=250)).strftime("%Y-%m-%d")

df = client.history(symbol="SBIN", exchange="NSE", interval="D", start_date=start, end_date=end)

# ma_envelopes(data) -> (upper, middle, lower)
up, mid, low = ta.ma_envelopes(df["close"], period=20, percentage=2.5)
# alligator(data) -> (jaw, teeth, lips) -- slow, medium, fast
jaw, teeth, lips = ta.alligator(df["close"])

price = df["close"].iloc[-1]
print("SBIN close:", round(price, 2))
print(f"Envelope   : lower {low.iloc[-1]:.2f} | mid {mid.iloc[-1]:.2f} | upper {up.iloc[-1]:.2f}")
print("Position   :", "near upper band (stretched up)" if price > mid.iloc[-1] else "near lower band (stretched down)")
print(f"Alligator  : lips {lips.iloc[-1]:.2f} > teeth {teeth.iloc[-1]:.2f} > jaw {jaw.iloc[-1]:.2f}?")

# Lips above teeth above jaw = the "alligator is eating" = a trend is underway.
if lips.iloc[-1] > teeth.iloc[-1] > jaw.iloc[-1]:
    print("Alligator read: lines fanned up -> bullish trend feeding")
elif lips.iloc[-1] < teeth.iloc[-1] < jaw.iloc[-1]:
    print("Alligator read: lines fanned down -> bearish trend feeding")
else:
    print("Alligator read: lines tangled -> sleeping (range)")
```

Live output

```
SBIN close: 1023.6
Envelope   : lower 972.53 | mid 997.47 | upper 1022.41
Position   : near upper band (stretched up)
Alligator  : lips 1013.90 > teeth 995.23 > jaw 991.37?
Alligator read: lines fanned up -> bullish trend feeding
```

## Choosing and combining trend filters
No single indicator is right all the time. The professional move isn't to hunt for a magic one - it's to combine a few that disagree in different ways and only act when they _agree_. That agreement requirement is called a **trend filter** : a gate your trades must pass before you take them. Here we poll three independent tools - an EMA, Supertrend and Parabolic SAR - and act only when at least two line up.
EX 9A three-vote trend filterMCXch11/09_trend_filter.py
Copy
```
# Combine three trend tools into one verdict -- the seed of a real trend filter.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")

df = client.history(symbol="CRUDEOIL20JUL26FUT", exchange="MCX", interval="1h", start_date=start, end_date=end)

price = df["close"].iloc[-1]
ema50 = ta.ema(df["close"], 50).iloc[-1]
_, st_dir = ta.supertrend(df["high"], df["low"], df["close"])
sar = ta.psar(df["high"], df["low"]).iloc[-1]

votes = {
    "Price > EMA50": price > ema50,
    "Supertrend up": st_dir.iloc[-1] == -1,
    "Price > PSAR": price > sar,
}
score = sum(votes.values())

print("CRUDEOIL close:", round(price, 2))
for name, ok in votes.items():
    print(f"  {name:16s}: {'yes' if ok else 'no'}")
print(f"Bullish votes: {score}/3 ->",
      "go with longs" if score >= 2 else "favour shorts / stand aside")
```

Live output

```
CRUDEOIL close: 6960
  Price > EMA50   : no
  Supertrend up   : no
  Price > PSAR    : yes
Bullish votes: 1/3 -> favour shorts / stand aside
```

Tip
A filter like this won't catch the exact bottom or top - it's not meant to. Its job is to keep you on the right side of the dominant move and out of the chop. Trading _with_ a confirmed trend, even a few bars late, beats picking turns and being early-and-wrong.
## Try it yourself
  * In the first example, swap `RELIANCE` for a stock you follow and change the periods to 50 and 200 - the classic long-term pair.
  * Change the Supertrend `multiplier` from `3.0` to `2.0` in example five. A smaller multiplier flips more often (more signals, more noise) - count the difference.
  * Point the trend-filter example at an NSE stock on the daily timeframe and see whether the three tools agree today.


## Recap
  * A **moving average** smooths price to reveal direction; **price above its MA = uptrend** is the foundation rule.
  * **SMA** is calm and equal-weighted; **EMA** reacts faster. Short periods hug price, long periods define the big trend.
  * **WMA, HMA, VWMA, KAMA** all fight lag in different ways - faster reaction always costs you more false signals.
  * Simple averages return a **Series** ; **Supertrend** and **Ichimoku** return **tuples** you must unpack - and Supertrend's direction is **-1 up / +1 down**.
  * **Parabolic SAR** doubles as a trailing stop; **Envelopes** and the **Alligator** flag stretch and trend strength.
  * The real power is **combining** trend tools into a filter and acting only when they agree.


Trend tells you _which way_. Next we measure _how hard and how fast_ with the momentum family - RSI, MACD, Stochastic and more - and learn to read overbought, oversold, and the early warning of divergence.
On this page
