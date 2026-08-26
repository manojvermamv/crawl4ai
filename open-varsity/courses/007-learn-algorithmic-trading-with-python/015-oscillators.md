Chapters
Module C · Technical Indicators - Chapter 15
# Oscillators
Bounded momentum tools: ROC, TRIX, Awesome Oscillator, StochRSI, Vortex and friends.
NSEMCX
What you'll learn
  * ·ROC & CMO
  * ·TRIX
  * ·Awesome Oscillator
  * ·Stochastic RSI
  * ·Vortex & TSI
  * ·Choppiness Index


An **oscillator** is any indicator that swings back and forth around a centre line or between two limits, like a pendulum. Instead of telling you the price, it tells you the _state_ of momentum - is the move speeding up, slowing down, stretched too far, or running out of steam? You've already met a few oscillators in passing (RSI, Stochastic, MACD). This chapter gathers the rest of the toolbox and, more importantly, teaches you the one distinction that decides whether an oscillator helps you or hurts you: **bounded versus unbounded** , and **trend versus range**.
Here's why that matters. Some oscillators have hard limits - they can never go above 100 or below 0 (or -100 to +100). Those **bounded** oscillators are brilliant for spotting _overbought_ and _oversold_ extremes in a sideways market, where price keeps bouncing between levels. But in a strong trend they betray you: they pin themselves at "overbought" and stay there for weeks while the price keeps climbing. **Unbounded** oscillators have no ceiling; they measure raw momentum and shine at confirming the _strength_ of a trend rather than calling its turns. Use the wrong type in the wrong market and you'll fight the tape. By the end of this chapter you'll know which is which.
As always, each script starts with `from openalgo import api, ta`. We verified every name and return type against the live server. One detail to keep in your pocket: most of these return a pandas **Series** , but a couple return a **NumPy array** or a **tuple** of Series - you'll see it printed, and we handle each correctly.
## Bounded vs unbounded, side by side
Let's make the core distinction concrete by computing two oscillators on the same stock. **Rate of Change (ROC)** is the purest momentum measure: the percentage the price has moved over N bars. It has no limits - a violent rally can push it to +30%, a crash to -40%. That makes it **unbounded**. The **Chande Momentum Oscillator (CMO)** measures something similar but normalises it onto a fixed -100 to +100 scale, making it **bounded** with natural overbought (above 50) and oversold (below -50) zones.
EX 1ROC and CMO: unbounded vs boundedNSEch15/01_roc_cmo.py
Copy
```
# ROC vs CMO: an UNBOUNDED oscillator next to a BOUNDED one.
import os
from datetime import datetime, timedelta

import numpy as np
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")
df = client.history(symbol="RELIANCE", exchange="NSE", interval="D", start_date=start, end_date=end)

# ROC (Rate of Change) returns a NUMPY ARRAY - it has no fixed ceiling.
roc = ta.roc(df["close"], 12)
print("ta.roc returns a", type(roc).__name__)

# CMO (Chande Momentum Oscillator) returns a SERIES bounded between -100 and +100.
df["CMO"] = ta.cmo(df["close"], 14)
print("ta.cmo returns a", type(df["CMO"]).__name__)

print(f"\nLatest ROC(12): {float(np.asarray(roc)[-1]):+.2f}%   (unbounded - just a % change)")
print(f"Latest CMO(14): {df['CMO'].iloc[-1]:+.2f}     (bounded -100..+100)")
print("CMO zone:", "overbought (>50)" if df["CMO"].iloc[-1] > 50
      else "oversold (<-50)" if df["CMO"].iloc[-1] < -50 else "neutral")
```

Live output

```
ta.roc returns a ndarray
ta.cmo returns a Series

Latest ROC(12): +1.16%   (unbounded - just a % change)
Latest CMO(14): -3.59     (bounded -100..+100)
CMO zone: neutral
```

Notice the printed types: `ta.roc(...)` hands back a **NumPy array** (so we wrap it in `np.asarray(...)[-1]` to read the last value), while `ta.cmo(...)` returns a **Series** we can drop straight into the DataFrame. Small detail, but knowing the return type saves you a confusing error later.
Key idea
**The golden rule of oscillators.** Bounded oscillators (CMO, MFI, Stochastic, Ultimate, StochRSI) excel at calling reversals in a **range**. Unbounded ones (ROC, AO, MACD, TSI) excel at confirming momentum in a **trend**. Before you read any oscillator, ask: _is this market trending or ranging?_ The Choppiness Index at the end of this chapter answers exactly that question.
## TRIX: smoothing away the noise
**TRIX** is the rate of change of a _triple_ exponentially smoothed price. All that smoothing is deliberate: it strips out the small wiggles that trigger false signals, leaving a clean line that oscillates around zero. It's **unbounded** , and the classic signal is a **zero-line cross** - TRIX rising above zero suggests building bullish momentum, dropping below suggests bearish. The trade-off for its smoothness is lag: TRIX is slower to react, which is fine if you want to ride trends and skip the chop.
EX 2TRIX, the triple-smoothed oscillatorNSEch15/02_trix.py
Copy
```
# TRIX: a triple-smoothed momentum oscillator that filters out noise.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=200)).strftime("%Y-%m-%d")
df = client.history(symbol="TCS", exchange="NSE", interval="D", start_date=start, end_date=end)

# TRIX = rate of change of a triple-EMA-smoothed price. Heavy smoothing = few false signals.
df["TRIX"] = ta.trix(df["close"], 15)

trix = df["TRIX"].iloc[-1]
prev = df["TRIX"].iloc[-2]
print(df[["close", "TRIX"]].tail(5).round(4))
print(f"\nLatest TRIX(15): {trix:+.4f}")
print("Momentum:", "positive (above zero)" if trix > 0 else "negative (below zero)")
# A zero-line cross is the classic TRIX signal.
print("Crossed zero this bar:", (prev <= 0 < trix) or (prev >= 0 > trix))
```

Live output

```
close     TRIX
timestamp                  
2026-06-17  2223.0 -35.4775
2026-06-18  2203.3 -34.8085
2026-06-19  2125.0 -34.5504
2026-06-22  2127.8 -34.4854
2026-06-23  2060.0 -35.1177

Latest TRIX(15): -35.1177
Momentum: negative (below zero)
Crossed zero this bar: False
```

## Ultimate Oscillator: three timeframes in one
A common complaint about single-period oscillators is that they fire false divergences. The **Ultimate Oscillator (UO)** tackles this by blending _three_ lookback periods - short (7), medium (14) and long (28) - into one **bounded** 0-to-100 line. Because it samples several horizons, a reading at an extreme is less likely to be a fluke. Above 70 is overbought, below 30 oversold. We run it on a silver future to keep the commodity flavour in the mix.
EX 3Ultimate Oscillator across three periodsMCXch15/03_ultimate_oscillator.py
Copy
```
# Ultimate Oscillator: blends three timeframes to cut down on false divergences.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=150)).strftime("%Y-%m-%d")
df = client.history(symbol="SILVERM30JUN26FUT", exchange="MCX", interval="D", start_date=start, end_date=end)

# UO weights short (7), medium (14) and long (28) periods - bounded 0..100.
df["UO"] = ta.ultimate_oscillator(df["high"], df["low"], df["close"])

uo = df["UO"].iloc[-1]
print(df[["close", "UO"]].tail(5).round(2))
print(f"\nLatest Ultimate Oscillator: {uo:.1f}")
print("Zone:", "overbought (>70)" if uo > 70 else "oversold (<30)" if uo < 30 else "neutral (30-70)")
```

Live output

```
close     UO
timestamp                
2026-06-17  255270  52.74
2026-06-18  242301  48.76
2026-06-19  237094  48.33
2026-06-22  238233  43.33
2026-06-23  231560  38.84

Latest Ultimate Oscillator: 38.8
Zone: neutral (30-70)
```

## Awesome Oscillator: momentum as a histogram
Bill Williams' **Awesome Oscillator (AO)** measures momentum as the gap between a fast (5-period) and slow (34-period) simple moving average of each bar's _midpoint_ - note it uses only high and low, never the close. It's **unbounded** and oscillates around zero. Traders read two things: which **side of zero** it's on (above is bullish, below bearish), and whether the current bar is **higher or lower** than the last (the famous green/red histogram). A flip from red to green above zero is a momentum kick worth noticing.
EX 4Awesome Oscillator and its histogramNSEch15/04_awesome_oscillator.py
Copy
```
# Awesome Oscillator (AO): momentum as the gap between two midpoint averages.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")
df = client.history(symbol="HDFCBANK", exchange="NSE", interval="D", start_date=start, end_date=end)

# AO = SMA(5) of the bar midpoint minus SMA(34). Uses high & low only. Unbounded, oscillates around 0.
df["AO"] = ta.awesome_oscillator(df["high"], df["low"])

ao = df["AO"].iloc[-1]
prev = df["AO"].iloc[-2]
print(df[["close", "AO"]].tail(5).round(2))
print(f"\nLatest AO: {ao:+.2f}")
print("Side of zero:", "bullish (above)" if ao > 0 else "bearish (below)")
print("Histogram bar color:", "green (rising)" if ao > prev else "red (falling)")
```

Live output

```
close     AO
timestamp               
2026-06-17  787.1   8.77
2026-06-18  799.0  17.75
2026-06-19  779.8  21.17
2026-06-22  786.4  21.35
2026-06-23  772.9  20.65

Latest AO: +20.65
Side of zero: bullish (above)
Histogram bar color: red (falling)
```

## PPO: MACD you can compare across symbols
If you know MACD, you know the **Percentage Price Oscillator (PPO)** - it's the same fast-minus-slow EMA idea, but expressed as a _percentage_ of the slow EMA instead of an absolute price difference. That one change is powerful: because MACD is in price units, a MACD of 50 means something totally different for a stock at 200 versus a future at 50,000. PPO's percentage scale lets you compare momentum _across_ instruments fairly. Like MACD, it returns a **tuple** of three Series: the PPO line, its signal line, and the histogram between them.
EX 5Percentage Price Oscillator on a Bank Nifty futureNFOch15/05_ppo.py
Copy
```
# PPO: MACD expressed as a PERCENTAGE, so you can compare across symbols.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=150)).strftime("%Y-%m-%d")
df = client.history(symbol="BANKNIFTY30JUN26FUT", exchange="NFO", interval="D", start_date=start, end_date=end)

# PPO returns a TUPLE: (ppo_line, signal_line, histogram). Values are percentages.
ppo_line, signal_line, histogram = ta.ppo(df["close"])
df["PPO"] = ppo_line
df["PPO_Signal"] = signal_line
df["PPO_Hist"] = histogram

print(df[["close", "PPO", "PPO_Signal", "PPO_Hist"]].tail(5).round(3))
print(f"\nLatest PPO: {df['PPO'].iloc[-1]:+.3f}%   Signal: {df['PPO_Signal'].iloc[-1]:+.3f}%")
print("Momentum:", "bullish (PPO above signal)" if df["PPO"].iloc[-1] > df["PPO_Signal"].iloc[-1]
      else "bearish (PPO below signal)")
```

Live output

```
close    PPO  PPO_Signal  PPO_Hist
timestamp                                       
2026-06-17  57588.2  1.029       0.394     0.636
2026-06-18  57996.0  1.230       0.561     0.669
2026-06-19  57861.6  1.352       0.719     0.633
2026-06-22  58011.4  1.453       0.866     0.587
2026-06-23  57185.0  1.398       0.973     0.426

Latest PPO: +1.398%   Signal: +0.973%
Momentum: bullish (PPO above signal)
```

Tip
When an indicator returns a tuple, unpack it on one line: `ppo_line, signal_line, histogram = ta.ppo(close)`. If you only grab the first value by mistake, you'll silently lose the signal line and histogram. The number of items in the tuple is fixed by the indicator - PPO and MACD give three; StochRSI, TSI and Vortex give two.
## DPO: stripping out the trend to see the cycle
The **Detrended Price Oscillator (DPO)** is the odd one out here, and that's the point. Every other oscillator in this chapter is about _momentum_. DPO is about _cycles_. It subtracts a displaced moving average from price, which deliberately **removes the trend** so you can see the shorter rhythmic swings - the peaks and troughs - underneath. It is _not_ meant to predict direction; it's meant to estimate where you are in a price cycle. A positive DPO means price is above its detrended average (heading toward a cyclical peak), negative means below (toward a trough).
EX 6Detrended Price Oscillator reveals cyclesNSEch15/06_dpo.py
Copy
```
# DPO: removes the trend so you can see the price CYCLE underneath.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=150)).strftime("%Y-%m-%d")
df = client.history(symbol="INFY", exchange="NSE", interval="D", start_date=start, end_date=end)

# DPO (Detrended Price Oscillator) subtracts a shifted moving average. It is NOT a momentum
# indicator - it strips out the trend to expose short cycles (peaks and troughs).
df["DPO"] = ta.dpo(df["close"], period=20)

dpo = df["DPO"].iloc[-1]
print(df[["close", "DPO"]].tail(5).round(2))
print(f"\nLatest DPO(20): {dpo:+.2f}")
print("Cycle position:", "above its detrended average (toward a peak)" if dpo > 0
      else "below its detrended average (toward a trough)")
```

Live output

```
close     DPO
timestamp                 
2026-06-17  1157.7   14.41
2026-06-18  1127.5  -17.97
2026-06-19  1051.4  -95.74
2026-06-22  1065.4  -83.44
2026-06-23  1029.0 -120.25

Latest DPO(20): -120.25
Cycle position: below its detrended average (toward a trough)
```

## Aroon Oscillator: how fresh is the trend?
The **Aroon Oscillator** asks a clever question: _how many bars ago did we make a new high, versus a new low?_ It's the difference between Aroon Up and Aroon Down, giving a **bounded** -100 to +100 line. A reading near +100 means new highs are very recent (a fresh, strong uptrend); near -100 means new lows dominate (a downtrend); near zero means neither - a directionless market. It uses only high and low, and it's excellent for confirming whether a trend is young and alive or stale.
EX 7Aroon Oscillator on goldMCXch15/07_aroon_oscillator.py
Copy
```
# Aroon Oscillator: how recently did we make a new high vs a new low?
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")
df = client.history(symbol="GOLDM03JUL26FUT", exchange="MCX", interval="D", start_date=start, end_date=end)

# Aroon Oscillator = Aroon Up minus Aroon Down. Bounded -100..+100 (uses high & low, no close).
df["AROON_OSC"] = ta.aroon_oscillator(df["high"], df["low"], period=14)

osc = df["AROON_OSC"].iloc[-1]
print(df[["close", "AROON_OSC"]].tail(5).round(1))
print(f"\nLatest Aroon Oscillator: {osc:+.1f}")
print("Trend:", "strong up (recent new highs)" if osc > 50
      else "strong down (recent new lows)" if osc < -50 else "weak / no clear trend")
```

Live output

```
close  AROON_OSC
timestamp                    
2026-06-17  151747      -64.3
2026-06-18  147424      -64.3
2026-06-19  145221      -92.9
2026-06-22  146125      -92.9
2026-06-23  144433      -92.9

Latest Aroon Oscillator: -92.9
Trend: strong down (recent new lows)
```

## Stochastic RSI: an oscillator of an oscillator
**Stochastic RSI** is exactly what it sounds like - it applies the Stochastic formula _to RSI values_ rather than to price. The effect is a turbocharged, very sensitive **bounded** 0-to-100 oscillator that reaches its extremes far more often than RSI alone. It returns a **tuple** of two lines (%K and %D, like the regular Stochastic). That sensitivity is a double-edged sword: great for precise timing in a range, but noisy and prone to whipsaws in a trend. Treat it as a fine-tuning tool, not a standalone system.
EX 8Stochastic RSI for sensitive timingNSEch15/08_stochrsi.py
Copy
```
# Stochastic RSI: an oscillator OF an oscillator - extra sensitive timing.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=150)).strftime("%Y-%m-%d")
df = client.history(symbol="ICICIBANK", exchange="NSE", interval="D", start_date=start, end_date=end)

# StochRSI returns a TUPLE (%K, %D), both bounded 0..100. It applies the Stochastic
# formula to RSI values, so it moves faster and hits extremes more often than RSI alone.
k, d = ta.stochrsi(df["close"])
df["StochRSI_K"] = k
df["StochRSI_D"] = d

kv, dv = df["StochRSI_K"].iloc[-1], df["StochRSI_D"].iloc[-1]
print(df[["close", "StochRSI_K", "StochRSI_D"]].tail(5).round(1))
print(f"\nLatest %K: {kv:.1f}   %D: {dv:.1f}")
print("Zone:", "overbought (>80)" if kv > 80 else "oversold (<20)" if kv < 20 else "neutral")
print("Short-term:", "%K above %D (bullish)" if kv > dv else "%K below %D (bearish)")
```

Live output

```
close  StochRSI_K  StochRSI_D
timestamp                                 
2026-06-17  1336.8        88.8        91.8
2026-06-18  1342.3        92.1        90.9
2026-06-19  1346.5        95.0        92.0
2026-06-22  1352.4        97.8        95.0
2026-06-23  1335.5        89.0        93.9

Latest %K: 89.0   %D: 93.9
Zone: overbought (>80)
Short-term: %K below %D (bearish)
```

## True Strength Index: clean, double-smoothed momentum
The **True Strength Index (TSI)** double-smooths momentum to produce a clean line that, like TRIX, oscillates around zero - but it comes with its own **signal line** for crossover trades. Above zero is bullish bias, below is bearish; TSI crossing above its signal line is a long trigger, below is a short. The double smoothing makes it far less jumpy than raw ROC, which is why trend traders like it. It returns a **tuple** of (TSI line, signal line).
EX 9True Strength Index with a signal lineNSEch15/09_tsi.py
Copy
```
# True Strength Index (TSI): double-smoothed momentum with a signal line.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=200)).strftime("%Y-%m-%d")
df = client.history(symbol="RELIANCE", exchange="NSE", interval="D", start_date=start, end_date=end)

# TSI returns a TUPLE (tsi_line, signal_line). Double smoothing makes it cleaner than raw momentum.
tsi_line, signal_line = ta.tsi(df["close"])
df["TSI"] = tsi_line
df["TSI_Signal"] = signal_line

t, s = df["TSI"].iloc[-1], df["TSI_Signal"].iloc[-1]
print(df[["close", "TSI", "TSI_Signal"]].tail(5).round(2))
print(f"\nLatest TSI: {t:+.2f}   Signal: {s:+.2f}")
print("Bias:", "bullish (TSI above zero)" if t > 0 else "bearish (TSI below zero)")
print("Trigger:", "TSI above signal (long)" if t > s else "TSI below signal (short)")
```

Live output

```
close    TSI  TSI_Signal
timestamp                            
2026-06-17  1332.7 -16.47      -19.36
2026-06-18  1328.1 -13.75      -18.56
2026-06-19  1309.5 -12.85      -17.74
2026-06-22  1326.5 -10.59      -16.72
2026-06-23  1306.0 -10.27      -15.80

Latest TSI: -10.27   Signal: -15.80
Bias: bearish (TSI below zero)
Trigger: TSI above signal (long)
```

## Vortex Indicator: a crossover trend system
The **Vortex Indicator (VI)** is built from two lines that capture upward (VI+) and downward (VI-) price movement. The signal is their **crossover** : when VI+ rises above VI-, an uptrend is taking hold; when VI- leads, a downtrend. The wider the gap between the two, the stronger the trend. The formula is short enough that we build both lines directly with pandas in the example - summing each move over the period and dividing by the summed true range - so you can see exactly what VI+ and VI- measure. This is a trend-following oscillator, not an overbought/oversold one - don't fade it.
EX 10Vortex Indicator crossover on crude oilMCXch15/10_vortex.py
Copy
```
# Vortex Indicator (VI): two lines whose crossover marks a trend change.
import os
from datetime import datetime, timedelta

import pandas as pd
from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=150)).strftime("%Y-%m-%d")
df = client.history(symbol="CRUDEOIL20JUL26FUT", exchange="MCX", interval="D", start_date=start, end_date=end)

# Vortex is two lines built from up-move (VI+) and down-move (VI-) vs the true range.
# We build it directly so you can see the formula: sum the moves over N bars, divide by
# the summed true range. When VI+ is above VI-, an uptrend; below, a downtrend.
period = 14
h, low_, c = df["high"], df["low"], df["close"]
prev_c = c.shift(1)
true_range = pd.concat([h - low_, (h - prev_c).abs(), (low_ - prev_c).abs()], axis=1).max(axis=1)
vm_plus = (h - low_.shift(1)).abs()
vm_minus = (low_ - h.shift(1)).abs()
str_sum = true_range.rolling(period).sum()
df["VI_Plus"] = vm_plus.rolling(period).sum() / str_sum
df["VI_Minus"] = vm_minus.rolling(period).sum() / str_sum

p, m = df["VI_Plus"].iloc[-1], df["VI_Minus"].iloc[-1]
print(df[["close", "VI_Plus", "VI_Minus"]].tail(5).round(3))
print(f"\nLatest VI+: {p:.3f}   VI-: {m:.3f}")
print("Trend:", "up (VI+ leads)" if p > m else "down (VI- leads)")
print("Spread:", f"{abs(p - m):.3f}  (wider = stronger trend)")
```

Live output

```
close  VI_Plus  VI_Minus
timestamp                           
2026-06-17   7158    0.732     1.073
2026-06-18   7054    0.710     1.085
2026-06-19   7262    0.701     1.165
2026-06-22   6983    0.672     1.128
2026-06-23   6957    0.596     1.239

Latest VI+: 0.596   VI-: 1.239
Trend: down (VI- leads)
Spread: 0.643  (wider = stronger trend)
```

## Choppiness Index: the regime detector
We end with the most strategically important oscillator of the lot. The **Choppiness Index (CHOP)** does not tell you direction at all - it tells you whether the market is **trending or ranging**. It's **bounded** 0 to 100: readings **above 61.8** mean the market is choppy and sideways, **below 38.2** mean a strong directional trend is in force. This is the answer to the question we posed at the top of the chapter. Use CHOP as a _filter_ : in choppy conditions, favour your range tools (Stochastic, CMO, UO at extremes); in trending conditions, favour your trend tools (TRIX, TSI, Vortex, Aroon) and ignore overbought/oversold warnings.
EX 11Choppiness Index picks the regimeNFOch15/11_choppiness.py
Copy
```
# Choppiness Index: is the market TRENDING or RANGING right now?
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")
df = client.history(symbol="NIFTY30JUN26FUT", exchange="NFO", interval="D", start_date=start, end_date=end)

# CHOP is bounded 0..100 but it measures TREND vs RANGE, not direction.
# High (>61.8) = choppy/sideways; low (<38.2) = strong directional trend.
df["CHOP"] = ta.chop(df["high"], df["low"], df["close"], period=14)

chop = df["CHOP"].iloc[-1]
print(df[["close", "CHOP"]].tail(5).round(1))
print(f"\nLatest Choppiness: {chop:.1f}")
if chop > 61.8:
    print("Regime: CHOPPY / sideways - favour range tools, avoid trend-following")
elif chop < 38.2:
    print("Regime: TRENDING strongly - favour trend-following, avoid mean-reversion")
else:
    print("Regime: in between - no clear edge for either style")
```

Live output

```
close  CHOP
timestamp                
2026-06-17  24094.0  52.4
2026-06-18  24192.5  47.0
2026-06-19  24056.9  46.0
2026-06-22  24123.8  43.5
2026-06-23  23810.0  43.0

Latest Choppiness: 43.0
Regime: in between - no clear edge for either style
```

Heads up
Never trade an oscillator blind to the regime. The single most common beginner mistake is shorting a stock because RSI or CMO says "overbought" - while it's in a roaring uptrend that keeps it overbought for a month. Check the Choppiness Index (or ADX, coming next chapter) first. Overbought/oversold signals are for **ranges** ; momentum and crossover signals are for **trends**.
## Try it yourself
  * Run the ROC/CMO example on a quietly ranging stock and then on a strongly trending one. Watch how CMO pins near its extreme during the trend while ROC keeps climbing - the bounded-vs-unbounded behaviour made visible.
  * Combine the Choppiness Index with the Vortex Indicator: print the Vortex signal _only_ on days when CHOP is below 38.2 (a confirmed trend). That's a regime-filtered trend system in a few lines.
  * Change the Stochastic RSI symbol to a commodity future and compare how often it reaches overbought versus how often plain RSI (from Chapter 12) does on the same data.


## Recap
  * An **oscillator** swings around a centre or between limits; it measures the _state_ of momentum, not the price itself.
  * **Bounded** oscillators (CMO, MFI, UO, Stochastic, StochRSI) call overbought/oversold extremes - best in a **range**.
  * **Unbounded** oscillators (ROC, AO, MACD, TRIX, TSI) measure raw momentum - best for confirming a **trend**.
  * Watch the **return type** : `ta.roc` gives a NumPy array; `ppo`, `stochrsi` and `tsi` give tuples; most others give a Series.
  * **PPO** is MACD as a percentage (comparable across symbols); **DPO** strips the trend to reveal cycles; **Vortex** and **Aroon** track trend direction and freshness.
  * The **Choppiness Index** is your regime detector - let it decide whether to use range tools or trend tools.


Next we round out the indicator library with statistical tools (regression, correlation, beta), hybrid trend systems (ADX, pivots, Parabolic SAR) and - most important of all - the utility helpers like crossover, exrem and valuewhen that turn any of these indicators into clean, executable trading signals.
On this page
