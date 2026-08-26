Chapters
Module C · Technical Indicators - Chapter 12
# Momentum Indicators
Measure speed and strength: RSI, MACD, Stochastic, CCI and more.
NSENFO
What you'll learn
  * ·RSI
  * ·MACD
  * ·Stochastic
  * ·CCI & Williams %R
  * ·Fisher Transform
  * ·Connors RSI


In the last chapter we answered _which way?_ Now we ask _how hard, and is it tiring?_ That's **momentum** - the speed and strength behind a price move. Trend tools tell you a stock is going up; momentum tools tell you whether the climb is accelerating, cruising, or running out of breath. Read together, they're far more powerful than either alone.
Most momentum tools are **oscillators** : they swing back and forth inside a fixed range (often 0-100) rather than drifting with price. That bounded range is what makes them useful - it gives you objective lines to call a move **overbought** (stretched too far up, due a pause or pullback) or **oversold** (stretched too far down, due a bounce). And when momentum quietly disagrees with price - a phenomenon called **divergence** - you get one of the most respected early-warning signals in all of trading.
As in Chapter 11 we import both pieces and mind the shapes:

```
from openalgo import api, ta

```

Some of these return a single **Series** (`rsi`, `cci`, `williams_r`, `crsi`, `bop`); others return a **tuple** you unpack (`macd` gives three lines, `stochastic` and `fisher` give two). We'll call it out each time.
## RSI: the momentum speedometer
The **Relative Strength Index (RSI)** is the most famous oscillator there is. It measures how much price has risen versus fallen over a window (default 14 bars) and squeezes the answer onto a 0-100 dial. The convention you'll see everywhere: **above 70 is overbought, below 30 is oversold** , and 50 is the dividing line between bullish and bearish momentum.
`ta.rsi(...)` returns a single Series.
EX 1RSI and its zonesNSEch12/01_rsi.py
Copy
```
# RSI: a 0-100 speedometer for momentum. Above 70 = overbought, below 30 = oversold.
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

df["RSI14"] = ta.rsi(df["close"], 14)
rsi = df["RSI14"].iloc[-1]

print("RELIANCE close:", round(df["close"].iloc[-1], 2))
print("RSI(14)       :", round(rsi, 2))

if rsi > 70:
    print("Zone: OVERBOUGHT -> momentum stretched up, watch for a pullback")
elif rsi < 30:
    print("Zone: OVERSOLD -> momentum stretched down, watch for a bounce")
else:
    print("Zone: NEUTRAL (30-70) -> no extreme; 50 is the bull/bear line")
```

Live output

```
RELIANCE close: 1306.0
RSI(14)       : 45.66
Zone: NEUTRAL (30-70) -> no extreme; 50 is the bull/bear line
```

Heads up
"Overbought" does **not** mean "sell now." In a strong trend, RSI can sit above 70 for weeks while price keeps climbing - shorting every overbought reading is a classic beginner's way to lose money fighting a trend. Treat the zones as _context_ , not triggers, and confirm with the trend tools from Chapter 11.
## MACD: momentum from two moving averages
The **MACD** (Moving Average Convergence Divergence) turns the moving averages you already know into a momentum tool. It subtracts a slow EMA from a fast one to get the **MACD line** , then smooths that into a **signal line** , and plots the gap between them as a **histogram**. When the MACD line is above its signal, momentum is bullish; the histogram shows whether that push is building or fading.
`ta.macd(...)` returns a **tuple of three** : macd line, signal line, histogram.
EX 2The three MACD outputsNSEch12/02_macd.py
Copy
```
# MACD: two EMAs turned into a momentum signal. Three outputs in one tuple.
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

# Returns a TUPLE: macd line, signal line, histogram.
macd_line, signal_line, hist = ta.macd(df["close"])

m = macd_line.iloc[-1]
s = signal_line.iloc[-1]
h = hist.iloc[-1]

print("TCS close   :", round(df["close"].iloc[-1], 2))
print(f"MACD line   : {m:8.2f}")
print(f"Signal line : {s:8.2f}")
print(f"Histogram   : {h:8.2f}  (MACD minus signal)")
print("Momentum:", "BULLISH (MACD above signal)" if m > s else "BEARISH (MACD below signal)")
print("Push:", "strengthening" if h > 0 else "weakening / negative")
```

Live output

```
TCS close   : 2060.0
MACD line   :   -59.34
Signal line :   -55.56
Histogram   :    -3.78  (MACD minus signal)
Momentum: BEARISH (MACD below signal)
Push: weakening / negative
```

### The MACD crossover signal
The classic MACD trade is the **crossover** : buy when the MACD line crosses _above_ its signal, sell when it crosses _below_. OpenAlgo gives you a dedicated helper for exactly this. `ta.crossover(a, b)` returns a **numpy array** (not a Series) of flags - a `1` on each bar where line `a` crosses above line `b`, `0` otherwise. Its mirror is `ta.crossunder`. These helpers will become the backbone of signal-building in Chapter 17.
EX 3Count MACD crossoversNFOch12/03_macd_cross.py
Copy
```
# A MACD crossover is the classic signal. crossover() returns a numpy array of 0/1 flags.
import os
from datetime import datetime, timedelta

import numpy as np
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d")

df = client.history(symbol="NIFTY30JUN26FUT", exchange="NFO", interval="5m", start_date=start, end_date=end)

macd_line, signal_line, _ = ta.macd(df["close"])

# crossover(a, b) -> numpy array, 1 on the bar where a crosses ABOVE b.
bull = ta.crossover(macd_line, signal_line)
bear = ta.crossunder(macd_line, signal_line)

print("NIFTY future 5m bars:", len(df))
print("Bullish MACD crosses:", int(np.nansum(bull)))
print("Bearish MACD crosses:", int(np.nansum(bear)))

last_state = "bullish" if macd_line.iloc[-1] > signal_line.iloc[-1] else "bearish"
print("Current MACD posture:", last_state)
```

Live output

```
NIFTY future 5m bars: 900
Bullish MACD crosses: 34
Bearish MACD crosses: 34
Current MACD posture: bearish
```

Key idea
Three different shapes already, and this is why we keep flagging them. `rsi` is a **Series** , `macd` is a **tuple of Series** , and `crossover` is a **numpy array**. Mixing them up - say, calling `.iloc[-1]` on the numpy array - is the single most common error in this module. When in doubt, `print(type(result))`.
## Stochastic: where does the close sit in its range?
The **Stochastic Oscillator** asks a simple question: within the high-low range of the last _N_ bars, where did price _close_? Near the top of the range (a reading near 100) means buyers dominated; near the bottom (near 0) means sellers did. It returns two lines: a fast **%K** and its smoothed average **%D**. The zones here are **above 80 overbought, below 20 oversold** , and a %K-crossing-%D is a momentum signal much like MACD's.
`ta.stochastic(...)` returns a **tuple** : `(%K, %D)`.
EX 4Stochastic %K and %DNSEch12/04_stochastic.py
Copy
```
# Stochastic: where does the close sit inside its recent range? Returns %K and %D.
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

# Returns a TUPLE: %K (fast) and %D (its smoothed average).
k, d = ta.stochastic(df["high"], df["low"], df["close"], k_period=14, d_period=3)

kv = k.iloc[-1]
dv = d.iloc[-1]
print("HDFCBANK close:", round(df["close"].iloc[-1], 2))
print(f"%K = {kv:6.2f}   %D = {dv:6.2f}")

if kv > 80:
    print("Zone: OVERBOUGHT (>80) -> close near top of its range")
elif kv < 20:
    print("Zone: OVERSOLD (<20) -> close near bottom of its range")
else:
    print("Zone: mid-range (20-80)")
print("Cross:", "%K above %D -> bullish tilt" if kv > dv else "%K below %D -> bearish tilt")
```

Live output

```
HDFCBANK close: 772.9
%K =  67.09   %D =  76.61
Zone: mid-range (20-80)
Cross: %K below %D -> bearish tilt
```

## CCI and Williams %R
Two more overbought/oversold gauges, each with its own scale. The **Commodity Channel Index (CCI)** is _unbounded_ and centred on zero: readings above **+100** signal a strong uptrend, below **-100** a strong downtrend, and the middle band is a range. **Williams %R** runs on a negative scale from 0 to -100, where **above -20 is overbought and below -80 is oversold** - it's essentially the Stochastic flipped upside down. Both are happy on commodities, so we test them on an MCX silver contract.
`ta.cci(...)` and `ta.williams_r(...)` each return a single Series.
EX 5CCI and Williams %RMCXch12/05_cci_williams.py
Copy
```
# CCI and Williams %R: two more overbought/oversold gauges, tested on MCX silver.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")

df = client.history(symbol="SILVERM30JUN26FUT", exchange="MCX", interval="D", start_date=start, end_date=end)

cci = ta.cci(df["high"], df["low"], df["close"], 20).iloc[-1]
wr = ta.williams_r(df["high"], df["low"], df["close"], 14).iloc[-1]

print("SILVERM close:", round(df["close"].iloc[-1], 1))
print(f"CCI(20)      : {cci:8.2f}")
print("  ->", "strong up (>+100)" if cci > 100 else "strong down (<-100)" if cci < -100 else "ranging (-100..+100)")
print(f"Williams %R  : {wr:8.2f}")
print("  ->", "overbought (>-20)" if wr > -20 else "oversold (<-80)" if wr < -80 else "mid-range")
```

Live output

```
SILVERM close: 231600
CCI(20)      :  -135.71
  -> strong down (<-100)
Williams %R  :   -95.10
  -> oversold (<-80)
```

## Fisher Transform: sharpening the turns
Price changes don't follow a tidy bell curve, which makes turning points fuzzy. The **Fisher Transform** mathematically reshapes price into something close to a normal distribution, with the happy side effect of turning gentle bends into **sharp, decisive peaks and troughs** - so reversals jump out. It returns the Fisher line plus a **trigger** (essentially the previous value); the line crossing its trigger after a deep extreme is the signal.
`ta.fisher(...)` takes **high and low** and returns a **tuple** : `(fisher, trigger)`.
EX 6Fisher Transform turning pointsNSEch12/06_fisher.py
Copy
```
# Fisher Transform: sharpens price into clear peaks so turns are easy to spot.
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

# Returns a TUPLE: fisher line and its trigger (the previous fisher value).
fisher, trigger = ta.fisher(df["high"], df["low"], length=9)

f = fisher.iloc[-1]
t = trigger.iloc[-1]
print("INFY close :", round(df["close"].iloc[-1], 2))
print(f"Fisher     : {f:7.3f}")
print(f"Trigger    : {t:7.3f}")

# A turn up through the trigger after a deep negative reading often marks a low.
print("Stretch:", "high (possible top)" if f > 1.5 else "low (possible bottom)" if f < -1.5 else "neutral")
print("Turn:", "fisher above trigger -> turning up" if f > t else "fisher below trigger -> turning down")
```

Live output

```
INFY close : 1029.0
Fisher     :  -1.483
Trigger    :  -1.172
Stretch: neutral
Turn: fisher below trigger -> turning down
```

## Connors RSI and Balance of Power
Two more specialists. **Connors RSI** is a composite built for short-term _mean reversion_ - it blends a very fast RSI, a streak measure, and a rank of recent change into one twitchy 0-100 line, where below 10 is deeply oversold and above 90 deeply overbought. **Balance of Power (BOP)** is different in spirit: bar by bar it measures whether the close finished nearer the high (buyers won) or the low (sellers won), on a scale of -1 to +1. Both return a single Series.
EX 7Connors RSI and Balance of PowerNSEch12/07_connors_bop.py
Copy
```
# Connors RSI (a mean-reversion RSI) and Balance of Power (buyers vs sellers each bar).
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

crsi = ta.crsi(df["close"]).iloc[-1]
bop = ta.bop(df["open"], df["high"], df["low"], df["close"]).iloc[-1]

print("ICICIBANK close:", round(df["close"].iloc[-1], 2))
print(f"Connors RSI    : {crsi:6.2f}")
# Connors RSI is twitchy: <10 is deeply oversold, >90 deeply overbought.
print("  ->", "deeply oversold (<10)" if crsi < 10 else "deeply overbought (>90)" if crsi > 90 else "neutral zone")
print(f"Balance of Power: {bop:6.3f}  (range -1 to +1)")
print("  ->", "buyers in control" if bop > 0 else "sellers in control")
```

Live output

```
ICICIBANK close: 1335.5
Connors RSI    :  25.47
  -> neutral zone
Balance of Power: -0.598  (range -1 to +1)
  -> sellers in control
```

## Divergence: the early warning
Here's the idea that makes momentum tools special. Normally price and momentum rise together. But sometimes price grinds to a **new high while the oscillator makes a _lower_ high** - the move is happening on weaker and weaker fuel. That's **bearish divergence** , a hint the uptrend is tiring. The mirror - price at a **lower low but the oscillator at a higher low** - is **bullish divergence** , a hint selling is exhausting. Divergence doesn't time the turn precisely, but it's a respected heads-up to tighten stops or take profit.
This example compares the last ten sessions against the ten before, on both price and RSI, to detect a divergence in plain Python.
EX 8Spot RSI divergenceNSEch12/08_divergence.py
Copy
```
# Divergence: price makes a new high but RSI doesn't -- a warning the push is tiring.
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
df["RSI"] = ta.rsi(df["close"], 14)

# Compare the last 10 bars with the 10 before them.
recent, prior = df.tail(10), df.iloc[-20:-10]
price_higher = recent["close"].max() > prior["close"].max()
rsi_higher = recent["RSI"].max() > prior["RSI"].max()

print("RELIANCE last 20 sessions")
print(f"Price high : prior {prior['close'].max():.2f} -> recent {recent['close'].max():.2f}")
print(f"RSI  high  : prior {prior['RSI'].max():.2f} -> recent {recent['RSI'].max():.2f}")

if price_higher and not rsi_higher:
    print("Bearish divergence: higher price, weaker RSI -> momentum fading")
elif not price_higher and rsi_higher:
    print("Bullish divergence: lower price, stronger RSI -> selling fading")
else:
    print("No divergence: price and RSI agree")
```

Live output

```
RELIANCE last 20 sessions
Price high : prior 1356.30 -> recent 1332.70
RSI  high  : prior 46.48 -> recent 52.52
Bullish divergence: lower price, stronger RSI -> selling fading
```

Tip
Divergence is a _warning_ , not a _signal_. A tiring trend can keep limping higher for a long time. The robust play is to wait for divergence **and** a confirming trigger - an RSI break back below 70, a MACD cross down, or price losing a moving average - before you act on it.
## Try it yourself
  * In the RSI example, switch the period from 14 to 7. A shorter RSI is far jumpier - watch how much more often it pokes into the overbought and oversold zones.
  * Point the Stochastic example at an MCX commodity like `GOLDM03JUL26FUT` and compare its zones to the equity version.
  * In the divergence example, widen the comparison windows from 10 bars to 20 and see whether the verdict changes.


## Recap
  * **Momentum** measures the _speed and strength_ of a move; most momentum tools are **oscillators** bounded in a fixed range.
  * **RSI** is the speedometer (70/30 zones); **MACD** turns two EMAs into a momentum signal with a famous **crossover**.
  * **Stochastic** locates the close within its range (80/20); **CCI** (±100) and **Williams %R** (-20/-80) are further overbought/oversold gauges.
  * **Fisher** sharpens turning points; **Connors RSI** is a fast mean-reversion gauge; **Balance of Power** weighs buyers vs sellers each bar.
  * Shapes matter: `rsi/cci/williams_r/crsi/bop` are **Series** , `macd` is a **3-tuple** , `stochastic/fisher` are **2-tuples** , and `crossover` is a **numpy array**.
  * **Divergence** - price and momentum disagreeing - is a powerful early warning, but confirm it before trading it.


We now know _which way_ (trend) and _how hard_ (momentum). The missing piece is _how wild_ - and that's the volatility family next: ATR, Bollinger Bands, Keltner and Donchian channels, the tools that size your risk and define the ranges you trade.
On this page
