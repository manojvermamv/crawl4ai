Chapters
Module C · Technical Indicators - Chapter 16
# Statistical, Hybrid & Utility Functions
Regression, correlation, ADX, pivots - plus the signal helpers you'll use everywhere.
NSENFO
What you'll learn
  * ·Linear regression & slope
  * ·Correlation & beta
  * ·ADX / DMI
  * ·Pivot points
  * ·crossover / crossunder
  * ·exrem / flip / valuewhen


This chapter wraps up the indicator library, and it earns its place as the most practical one of the three. We cover three families. First, **statistical** tools that treat price as data - regression lines, correlation, beta and variance - the language of quants and risk managers. Second, **hybrid** indicators like ADX, pivot points and Parabolic SAR that fuse trend, direction and levels into trading systems. And third - the part you'll reach for in _every_ strategy from here on - the **utility helpers** : `crossover`, `exrem`, `flip`, `valuewhen` and friends. Those small functions are the glue that turns a curvy indicator into a precise, de-duplicated, executable signal. Chapter 17 is built entirely on them, so we'll go slowly and make sure each one clicks.
Same setup as always - `from openalgo import api, ta` at the top of each script. A heads-up that pays off throughout: the statistical and hybrid indicators return pandas **Series** (or **tuples** of Series), but **the utility helpers return NumPy boolean or float arrays**. That difference dictates how you index into your DataFrame, so we print the return type in several examples to keep it front of mind.
## Part 1 - Statistical tools
### Linear regression and its slope
A **linear regression** fits the single straight line that sits closest to the price points over a window - the "line of best fit." Two outputs matter. `ta.linreg` gives you the line's value at each bar, a smoothed sense of fair value. `ta.lrslope` gives you the line's **slope** - its tilt - which is a clean, numeric read on trend direction and strength. A positive, steep slope is a strong uptrend; a slope near zero is a flat, directionless market. Slope is wonderful in code because it reduces "is this trending?" to a simple sign check.
EX 1Regression line and slopeNSEch16/01_linreg_slope.py
Copy
```
# Linear Regression line + slope: fit a straight line to price and read its tilt.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")
df = client.history(symbol="RELIANCE", exchange="NSE", interval="D", start_date=start, end_date=end)

# linreg fits a least-squares line; its endpoint is the "fair value" for that bar.
df["LINREG"] = ta.linreg(df["close"], 20)
# lrslope is the tilt of that line: positive = rising trend, negative = falling.
df["SLOPE"] = ta.lrslope(df["close"], period=20)

print(df[["close", "LINREG", "SLOPE"]].tail(5).round(2))
slope = df["SLOPE"].iloc[-1]
print(f"\nLatest slope: {slope:+.3f}")
print("Trend:", "up" if slope > 0 else "down" if slope < 0 else "flat")
gap = df["close"].iloc[-1] - df["LINREG"].iloc[-1]
print(f"Price is {gap:+.2f} vs its regression line ({'above' if gap > 0 else 'below'}).")
```

Live output

```
close   LINREG  SLOPE
timestamp                         
2026-06-17  1332.7  1279.28   3.96
2026-06-18  1328.1  1285.94   6.66
2026-06-19  1309.5  1288.58   2.65
2026-06-22  1326.5  1295.45   6.87
2026-06-23  1306.0  1300.16   4.71

Latest slope: +4.709
Trend: up
Price is +5.84 vs its regression line (above).
```

### Pearson correlation: do two things move together?
**Correlation** measures how tightly two series move in step, on a scale from **-1** (they move exactly opposite) through **0** (no relationship) to **+1** (they move in lockstep). It's the foundation of pair trading: you want two instruments with a high, _stable_ correlation, then trade the moments they temporarily drift apart. Here we measure two banking stocks against each other.
EX 2Correlation between two bank stocksNSEch16/02_correlation.py
Copy
```
# Pearson Correlation: do two instruments move together?
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=150)).strftime("%Y-%m-%d")
a = client.history(symbol="HDFCBANK", exchange="NSE", interval="D", start_date=start, end_date=end)
b = client.history(symbol="ICICIBANK", exchange="NSE", interval="D", start_date=start, end_date=end)

# correlation runs from -1 (move opposite) through 0 (unrelated) to +1 (move together).
corr = ta.correlation(a["close"], b["close"], 20)
a["CORR"] = corr

c = a["CORR"].iloc[-1]
print(a[["close", "CORR"]].tail(5).round(3))
print(f"\nLatest 20-day correlation HDFCBANK vs ICICIBANK: {c:+.3f}")
print("Reading:", "strongly linked" if c > 0.7 else "loosely linked" if c > 0.3
      else "barely related" if c > -0.3 else "moving opposite")
print("Pairs traders want a HIGH, stable correlation between the two legs.")
```

Live output

```
close   CORR
timestamp               
2026-06-17  787.1  0.609
2026-06-18  799.0  0.690
2026-06-19  779.8  0.719
2026-06-22  786.4  0.757
2026-06-23  772.9  0.789

Latest 20-day correlation HDFCBANK vs ICICIBANK: +0.789
Reading: strongly linked
Pairs traders want a HIGH, stable correlation between the two legs.
```

### Beta: how much does a stock amplify the market?
**Beta** is correlation's risk-focused cousin. It measures how much a stock moves _relative to the market_ (here, the NIFTY index). A beta of **1.0** means the stock moves with the index; **above 1** means it amplifies market moves (aggressive, high-risk); **below 1** means it's calmer than the index (defensive). Portfolio managers use beta to size positions and hedge: a high-beta stock needs a smaller position for the same market risk.
EX 3Beta of a stock versus NIFTYNSEINDEXch16/03_beta.py
Copy
```
# Beta: how much a stock amplifies the market's moves.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=200)).strftime("%Y-%m-%d")
stock = client.history(symbol="HDFCBANK", exchange="NSE", interval="D", start_date=start, end_date=end)
mkt = client.history(symbol="NIFTY", exchange="NSE_INDEX", interval="D", start_date=start, end_date=end)

# Beta measures the stock's volatility relative to the market (here NIFTY).
# Beta 1 = moves with the index; >1 = amplifies it; <1 = calmer than the index.
stock["BETA"] = ta.beta(stock["close"], mkt["close"], period=60)

b = stock["BETA"].iloc[-1]
print(stock[["close", "BETA"]].tail(5).round(3))
print(f"\nLatest 60-day Beta vs NIFTY: {b:.2f}")
print("Behaviour:", "amplifies the market (aggressive)" if b > 1.1
      else "tracks the market" if b > 0.9 else "calmer than the market (defensive)")
```

Live output

```
close   BETA
timestamp               
2026-06-17  787.1  0.050
2026-06-18  799.0  0.050
2026-06-19  779.8  0.050
2026-06-22  786.4  0.051
2026-06-23  772.9  0.049

Latest 60-day Beta vs NIFTY: 0.05
Behaviour: calmer than the market (defensive)
```

Note
Notice we fetch the market with `exchange="NSE_INDEX"` and symbol `NIFTY`. Index spot data is the right benchmark for beta and correlation. We line up the stock's closes against the index's closes over the same window - both must come from the same date range so the bars match up.
### Variance and the Time Series Forecast
**Variance** quantifies how spread out prices are around their average - it's literally the square of standard deviation. High variance means wild, scattered prices (more risk); low variance means tight, calm ones. The **Time Series Forecast (TSF)** is a neat companion: it extends the regression line one step into the future to _project_ the next bar's value. It's not a crystal ball, but comparing TSF to the actual close tells you whether price is running ahead of or behind its own trend.
EX 4Variance and a one-step forecastMCXch16/04_variance_tsf.py
Copy
```
# Variance and Time Series Forecast: dispersion now, projected value next.
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

# Variance measures how spread out prices are (the square of standard deviation).
df["VAR"] = ta.variance(df["close"], lookback=20)
# TSF projects the regression line one step ahead - a simple forecast of next value.
df["TSF"] = ta.tsf(df["close"], 14)

print(df[["close", "VAR", "TSF"]].tail(5).round(2))
print(f"\nLatest variance(20): {df['VAR'].iloc[-1]:,.2f}  (higher = wilder swings)")
print(f"Forecast for next bar (TSF): {df['TSF'].iloc[-1]:,.2f}")
print(f"Last actual close          : {df['close'].iloc[-1]:,.2f}")
```

Live output

```
close          VAR        TSF
timestamp                                 
2026-06-17  151747  20223306.93  147280.33
2026-06-18  147424  20749626.22  146719.37
2026-06-19  145221  22619066.05  145646.33
2026-06-22  146125  22241139.29  145233.56
2026-06-23  144287  23239059.42  144525.69

Latest variance(20): 23,239,059.42  (higher = wilder swings)
Forecast for next bar (TSF): 144,525.69
Last actual close          : 144,287.00
```

### Rolling median: the outlier-proof average
The **rolling median** is the middle value of a window. Its superpower is robustness: a single freak spike - a fat-finger print, a data glitch - can yank a moving _average_ around, but it barely budges the _median_. When your data is noisy, the median gives a steadier read of the "typical" price. We print it next to the mean so you can see them diverge when a spike hits.
EX 5Rolling median versus meanNSEch16/05_median.py
Copy
```
# Rolling Median: a "middle" price that ignores spikes and outliers.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
df = client.history(symbol="SBIN", exchange="NSE", interval="D", start_date=start, end_date=end)

# The median is the middle value of a window. Unlike the average, one freak
# spike can't drag it around - useful when data is noisy.
df["MEDIAN"] = ta.median(df["close"], 5)
df["MEAN"] = df["close"].rolling(5).mean()

print(df[["close", "MEDIAN", "MEAN"]].tail(5).round(2))
print(f"\nLatest 5-day median: {df['MEDIAN'].iloc[-1]:.2f}")
print(f"Latest 5-day mean  : {df['MEAN'].iloc[-1]:.2f}")
print("The median sits near the typical price even when a single day spikes.")
```

Live output

```
close   MEDIAN     MEAN
timestamp                            
2026-06-17  1026.50  1017.15  1016.10
2026-06-18  1042.70  1020.85  1024.50
2026-06-19  1035.10  1026.50  1028.09
2026-06-22  1040.75  1035.10  1032.07
2026-06-23  1023.60  1035.10  1033.73

Latest 5-day median: 1035.10
Latest 5-day mean  : 1033.73
The median sits near the typical price even when a single day spikes.
```

## Part 2 - Hybrid indicators
These combine multiple ideas into trading systems. Several return **tuples** , so unpack them carefully.
### ADX: how strong is the trend?
The **Average Directional Index (ADX)** answers a question most indicators ignore: not _which way_ is price going, but _how strongly_. It returns a **tuple** of three Series - `+DI`, `-DI` and `ADX`. The ADX line measures trend _strength_ (regardless of direction): above **25** is a strong trend, below **20** is a weak or ranging market. The `+DI` and `-DI` lines give _direction_ : whichever is on top tells you bull or bear. ADX is the classic regime filter - only take trend trades when ADX confirms a trend exists.
EX 6ADX trend strength and directionNSEch16/06_adx.py
Copy
```
# ADX: how STRONG is the trend (regardless of direction)?
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=150)).strftime("%Y-%m-%d")
df = client.history(symbol="TCS", exchange="NSE", interval="D", start_date=start, end_date=end)

# ADX returns a TUPLE: (+DI, -DI, ADX). ADX measures strength; +DI/-DI give direction.
di_plus, di_minus, adx = ta.adx(df["high"], df["low"], df["close"], period=14)
df["ADX"] = adx
df["DI+"] = di_plus
df["DI-"] = di_minus

a = df["ADX"].iloc[-1]
print(df[["close", "DI+", "DI-", "ADX"]].tail(5).round(1))
print(f"\nLatest ADX: {a:.1f}")
print("Trend strength:", "strong (>25)" if a > 25 else "weak / ranging (<20)" if a < 20 else "developing")
print("Direction:", "up (+DI leads)" if df["DI+"].iloc[-1] > df["DI-"].iloc[-1] else "down (-DI leads)")
```

Live output

```
close   DI+   DI-   ADX
timestamp                           
2026-06-17  2223.0  23.1  24.2  16.7
2026-06-18  2203.3  21.9  25.3  16.1
2026-06-19  2125.0  18.3  35.0  17.2
2026-06-22  2127.8  19.8  33.6  17.8
2026-06-23  2060.0  18.1  38.3  19.1

Latest ADX: 19.1
Trend strength: weak / ranging (<20)
Direction: down (-DI leads)
```

### Aroon: how fresh is the high or low?
**Aroon** returns a **tuple** of (Aroon Up, Aroon Down), each on a 0-to-100 scale. Aroon Up measures how recently a new high was made, Aroon Down a new low. When Up is high (above 70) and Down is low, you have a fresh, healthy uptrend; the reverse signals a downtrend. It's a different lens on the same idea as the Aroon _Oscillator_ you met last chapter, but here you see both raw lines.
EX 7Aroon Up and Down on a Nifty futureNFOch16/07_aroon.py
Copy
```
# Aroon Up / Aroon Down: time since the last new high vs new low.
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

# aroon returns a TUPLE (up, down). Each runs 0..100. High Up = recent new high.
aroon_up, aroon_down = ta.aroon(df["high"], df["low"], period=14)
df["Aroon_Up"] = aroon_up
df["Aroon_Down"] = aroon_down

up, dn = df["Aroon_Up"].iloc[-1], df["Aroon_Down"].iloc[-1]
print(df[["close", "Aroon_Up", "Aroon_Down"]].tail(5).round(0))
print(f"\nAroon Up: {up:.0f}   Aroon Down: {dn:.0f}")
print("Signal:", "strong uptrend" if up > 70 and dn < 30
      else "strong downtrend" if dn > 70 and up < 30 else "no dominant trend")
```

Live output

```
close  Aroon_Up  Aroon_Down
timestamp                                
2026-06-17  24094.0     100.0        71.0
2026-06-18  24192.0     100.0        64.0
2026-06-19  24057.0      93.0        57.0
2026-06-22  24124.0      86.0        50.0
2026-06-23  23810.0      79.0        43.0

Aroon Up: 79   Aroon Down: 43
Signal: no dominant trend
```

### Pivot points: yesterday's levels, today's map
**Pivot points** convert the previous bar's high, low and close into a central pivot plus three resistance and three support levels. They return a **7-tuple** - `pivot, r1, s1, r2, s2, r3, s3`. Day traders use them as a ready-made map of likely turning points: price above the pivot leans bullish, below leans bearish, and R1/S1 are the first places to watch for a reaction.
EX 8Pivot, support and resistance on crudeMCXch16/08_pivot_points.py
Copy
```
# Pivot Points: classic support/resistance levels from the prior bar.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d")
df = client.history(symbol="CRUDEOIL20JUL26FUT", exchange="MCX", interval="D", start_date=start, end_date=end)

# pivot_points returns a 7-TUPLE: pivot, r1, s1, r2, s2, r3, s3.
pivot, r1, s1, r2, s2, r3, s3 = ta.pivot_points(df["high"], df["low"], df["close"])
df["Pivot"], df["R1"], df["S1"] = pivot, r1, s1

last = df.iloc[-1]
print(df[["close", "S1", "Pivot", "R1"]].tail(3).round(1))
print(f"\nLatest close: {last['close']:.1f}")
print(f"  Resistance 1: {last['R1']:.1f}")
print(f"  Pivot       : {last['Pivot']:.1f}")
print(f"  Support 1   : {last['S1']:.1f}")
print("Bias:", "above pivot - bullish" if last["close"] > last["Pivot"] else "below pivot - bearish")
```

Live output

```
close      S1   Pivot      R1
timestamp                                
2026-06-19   7262  7145.3  7216.7  7333.3
2026-06-22   6983  6834.0  7108.0  7257.0
2026-06-23   6949  6884.7  6967.3  7031.7

Latest close: 6949.0
  Resistance 1: 7031.7
  Pivot       : 6967.3
  Support 1   : 6884.7
Bias: below pivot - bearish
```

### Parabolic SAR: a trend's trailing stop
**Parabolic SAR** ("stop and reverse") plots a series of dots that trail the price and tighten as a trend matures - a built-in trailing stop. When price is above the SAR you're long; when it crosses below, the SAR "flips" to the other side and you reverse. Here's a verification lesson worth its weight: the written docs hint that `ta.psar` returns a tuple, but **testing shows it returns a single Series** of stop levels. This is exactly why we test every indicator instead of trusting the manual.
EX 9Parabolic SAR trailing stopNSEch16/09_psar.py
Copy
```
# Parabolic SAR: a trailing stop that flips with the trend.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")
df = client.history(symbol="RELIANCE", exchange="NSE", interval="D", start_date=start, end_date=end)

# Despite the docs hinting at a tuple, ta.psar returns a SINGLE Series of stop levels.
# When price is above the SAR dot you're long; below, you're short.
df["SAR"] = ta.psar(df["high"], df["low"], acceleration=0.02, maximum=0.2)
print("ta.psar returns a", type(df["SAR"]).__name__)

last = df.iloc[-1]
print(df[["close", "SAR"]].tail(5).round(2))
print(f"\nClose: {last['close']:.2f}   SAR: {last['SAR']:.2f}")
print("Position:", "LONG (price above SAR)" if last["close"] > last["SAR"] else "SHORT (price below SAR)")
print(f"Trailing stop sits at {last['SAR']:.2f}.")
```

Live output

```
ta.psar returns a Series
             close      SAR
timestamp                  
2026-06-17  1332.7  1257.79
2026-06-18  1328.1  1262.36
2026-06-19  1309.5  1266.66
2026-06-22  1326.5  1272.38
2026-06-23  1306.0  1279.63

Close: 1306.00   SAR: 1279.63
Position: LONG (price above SAR)
Trailing stop sits at 1279.63.
```

Heads up
Documentation drifts; libraries change. Before you rely on any indicator's output, _call it once and check the type_ - `print(type(result).__name__)`. We caught Parabolic SAR returning a Series, not the tuple the docs implied. A five-second check saves a baffling crash when you try to unpack a Series into two variables.
### DMI and Williams Fractals
Two more in one script. The **Directional Movement Index (DMI)** is just the directional half of ADX - a **tuple** of (+DI, -DI) without the strength line. **Williams Fractals** mark local turning points: they return a **tuple** of two _boolean_ Series flagging swing highs (up-fractals) and swing lows (down-fractals). Those booleans are perfect for spotting the most recent swing high to place a stop or target.
EX 10DMI direction and Williams FractalsNSEch16/10_dmi_fractals.py
Copy
```
# DMI directional lines + Williams Fractals turning points.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")
df = client.history(symbol="INFY", exchange="NSE", interval="D", start_date=start, end_date=end)

# DMI returns a TUPLE (+DI, -DI) - the directional half of the ADX system.
di_plus, di_minus = ta.dmi(df["high"], df["low"], df["close"], period=14)
df["DI+"], df["DI-"] = di_plus, di_minus

# Fractals return a TUPLE of two BOOLEAN Series marking local tops and bottoms.
frac_up, frac_down = ta.fractals(df["high"], df["low"], periods=2)
df["FracUp"], df["FracDown"] = frac_up, frac_down

print(df[["close", "DI+", "DI-"]].tail(3).round(1))
print("Direction:", "bullish (+DI > -DI)" if df["DI+"].iloc[-1] > df["DI-"].iloc[-1] else "bearish (-DI > +DI)")
print(f"\nUp-fractals (swing highs) found: {int(df['FracUp'].sum())}")
print(f"Down-fractals (swing lows) found: {int(df['FracDown'].sum())}")
print("Last swing-high price:", round(df.loc[df["FracUp"], "high"].iloc[-1], 2))
```

Live output

```
close   DI+   DI-
timestamp                     
2026-06-19  1051.4  20.2  40.1
2026-06-22  1065.4  21.9  37.7
2026-06-23  1029.0  20.1  40.6
Direction: bearish (-DI > +DI)

Up-fractals (swing highs) found: 11
Down-fractals (swing lows) found: 8
Last swing-high price: 1162.5
```

## Part 3 - The utility helpers (the most important section)
Everything so far produces an _indicator_. The utilities below turn indicators into _signals_ - precise True/False events you can act on. They are the vocabulary of every strategy in this series, and Chapter 17 leans on them heavily. The crucial technical fact: **these all return NumPy arrays, not Series.** A boolean array can index a DataFrame directly (`df.index[buy]`), and you read its last value with `array[-1]` or `np.asarray(array)[-1]`.
### crossover and crossunder: the signal moment
A `crossover(a, b)` is **True only on the single bar** where line `a` crosses _above_ line `b`; `crossunder` is the mirror, where `a` crosses _below_ `b`. This is the heartbeat of moving-average systems. The key word is _moment_ : it fires once at the cross, not on every bar `a` stays above `b`. We use the returned boolean array to pull out the exact dates the crosses happened.
EX 11crossover and crossunder of two EMAsNSEch16/11_crossover.py
Copy
```
# crossover / crossunder: the moment one line crosses another.
import os
from datetime import datetime, timedelta

import numpy as np
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=200)).strftime("%Y-%m-%d")
df = client.history(symbol="RELIANCE", exchange="NSE", interval="D", start_date=start, end_date=end)

fast = ta.ema(df["close"], 10)
slow = ta.ema(df["close"], 20)

# crossover/crossunder return NUMPY BOOLEAN ARRAYS: True only on the bar of the cross.
buy = ta.crossover(fast, slow)
sell = ta.crossunder(fast, slow)
print("ta.crossover returns a", type(buy).__name__, "of dtype", buy.dtype)

print(f"\nBuy crosses (10 EMA over 20 EMA): {int(np.sum(buy))}")
print(f"Sell crosses (10 EMA under 20 EMA): {int(np.sum(sell))}")

# Use the boolean array to pull the dates/prices where a cross happened.
buy_dates = df.index[buy]
print("\nMost recent BUY cross dates:")
for d in buy_dates[-3:]:
    print(f"  {d.date()}  close {df.loc[d, 'close']:.2f}")
```

Live output

```
ta.crossover returns a ndarray of dtype bool

Buy crosses (10 EMA over 20 EMA): 4
Sell crosses (10 EMA under 20 EMA): 4

Most recent BUY cross dates:
  2025-12-12  close 1556.50
  2026-02-12  close 1448.90
  2026-04-29  close 1425.40
```

### highest and lowest: breakout levels
`highest(data, n)` and `lowest(data, n)` return the rolling maximum and minimum over the last `n` bars - the building blocks of breakout strategies (think Donchian channels). A classic 20-day breakout is simply _today's close above the prior 20-day high_. Note how we use the value **as of yesterday** (`[-2]`) so we're not comparing today's close to a high that already includes today.
EX 12Rolling highs and lows for breakoutsMCXch16/12_highest_lowest.py
Copy
```
# highest / lowest: rolling extremes that define breakout levels.
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
df = client.history(symbol="GOLDM03JUL26FUT", exchange="MCX", interval="D", start_date=start, end_date=end)

# highest/lowest return NUMPY ARRAYS of the rolling max/min over the window.
hh = ta.highest(df["high"], 20)
ll = ta.lowest(df["low"], 20)
print("ta.highest returns a", type(hh).__name__)

# A 20-day breakout: today's close pushes past the prior 20-day high.
prior_high = np.asarray(hh)[-2]   # the highest high as of yesterday
last_close = df["close"].iloc[-1]
print(f"\n20-day high (as of yesterday): {prior_high:,.0f}")
print(f"20-day low  (latest)         : {np.asarray(ll)[-1]:,.0f}")
print(f"Today's close                : {last_close:,.0f}")
print("Breakout:", "YES - new 20-day high" if last_close > prior_high else "no breakout yet")
```

Live output

```
ta.highest returns a ndarray

20-day high (as of yesterday): 160,033
20-day low  (latest)         : 143,518
Today's close                : 144,287
Breakout: no breakout yet
```

Key idea
**The look-ahead trap.** When checking a breakout, compare today's close to the highest high _up to yesterday_ (`highest(...)[-2]`), not the value that already includes today's bar. Mixing today's data into a level you then test today's price against is a subtle form of look-ahead bias that inflates backtest results. We'll hammer this point in the backtesting chapters.
### exrem: kill the duplicate signals
Here's a problem raw conditions create: a rule like "RSI is above 30" is True for _many_ bars in a row, so you'd get a flurry of buy signals when you only want the _first_. **`exrem(primary, secondary)`**(excess removal) fixes this - it keeps the first`primary` signal and _suppresses_ further ones until a `secondary` signal has occurred. In trade terms: buy once, ignore further buys until you've sold, then you may buy again. The example shows six raw sell signals collapsing to one clean one.
EX 13exrem removes repeated signalsNSEch16/13_exrem.py
Copy
```
# exrem: remove repeated signals so you act only on the FIRST one.
import os
from datetime import datetime, timedelta

import numpy as np
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=250)).strftime("%Y-%m-%d")
df = client.history(symbol="SBIN", exchange="NSE", interval="D", start_date=start, end_date=end)

rsi = ta.rsi(df["close"], 14)
# Raw conditions fire on EVERY bar the rule is true - lots of duplicates.
raw_buy = ta.crossover(rsi, np.full(len(rsi), 30.0))   # RSI crossing up through 30
raw_sell = ta.crossunder(rsi, np.full(len(rsi), 70.0))  # RSI crossing down through 70

# exrem keeps the first buy, ignores further buys until a sell has occurred (and vice versa).
clean_buy = ta.exrem(raw_buy, raw_sell)
clean_sell = ta.exrem(raw_sell, raw_buy)

print(f"Raw buy signals   : {int(np.sum(raw_buy))}")
print(f"Cleaned buy signals: {int(np.sum(clean_buy))}  (duplicates removed)")
print(f"Raw sell signals   : {int(np.sum(raw_sell))}")
print(f"Cleaned sell signals: {int(np.sum(clean_sell))}")
print("\nexrem stops you from buying again while you are already 'in'.")
```

Live output

```
Raw buy signals   : 2
Cleaned buy signals: 1  (duplicates removed)
Raw sell signals   : 6
Cleaned sell signals: 1

exrem stops you from buying again while you are already 'in'.
```

### flip: from signals to a holding state
`crossover` tells you _when_ to enter and exit, but often you want to know _"am I in a position right now?"_ on every bar. **`flip(on, off)`**does exactly that: it turns ON at the first`on` signal and stays ON until an `off` signal flips it back. The result is a continuous state series (1 = holding, 0 = flat) - the basis for computing how long a trade lasted and, later, for vectorised backtests.
EX 14flip turns signals into a position stateNSEch16/14_flip.py
Copy
```
# flip: turn entry/exit signals into a continuous "are we in?" state.
import os
from datetime import datetime, timedelta

import numpy as np
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=250)).strftime("%Y-%m-%d")
df = client.history(symbol="RELIANCE", exchange="NSE", interval="D", start_date=start, end_date=end)

fast, slow = ta.ema(df["close"], 10), ta.ema(df["close"], 20)
buy = ta.crossover(fast, slow)
sell = ta.crossunder(fast, slow)

# flip turns ON at the first buy and stays ON until a sell flips it OFF.
# It converts two momentary signals into a holding state (1 = in position, 0 = flat).
in_position = ta.flip(buy, sell)
print("ta.flip returns a", type(in_position).__name__)

df["InPos"] = np.asarray(in_position).astype(int)
days_in = int(df["InPos"].sum())
print(f"\nBars held long: {days_in} out of {len(df)}")
print("Currently:", "HOLDING long" if df["InPos"].iloc[-1] else "FLAT")
print("\nLast 8 bars (1 = in position):")
print(df[["close", "InPos"]].tail(8).round(2))
```

Live output

```
ta.flip returns a ndarray

Bars held long: 67 out of 168
Currently: FLAT

Last 8 bars (1 = in position):
             close  InPos
timestamp                
2026-06-12  1293.0      0
2026-06-15  1307.0      0
2026-06-16  1328.8      0
2026-06-17  1332.7      0
2026-06-18  1328.1      0
2026-06-19  1309.5      0
2026-06-22  1326.5      0
2026-06-23  1306.0      0
```

### valuewhen: remembering the entry
A strategy needs memory: _what was the price when I last entered?_ **`valuewhen(condition, series, n)`**returns the value of`series` at the bar the `condition` was last True. With `n=1` you get the most recent occurrence, `n=2` the one before, and so on. We use it to recall the entry price at the last EMA cross and compute the open trade's P&L - exactly how you'd track a live position's profit, stop and target.
EX 15valuewhen recalls the entry priceNSEch16/15_valuewhen.py
Copy
```
# valuewhen: recall the price at the last time a condition was true.
import os
from datetime import datetime, timedelta

import numpy as np
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=250)).strftime("%Y-%m-%d")
df = client.history(symbol="HDFCBANK", exchange="NSE", interval="D", start_date=start, end_date=end)

fast, slow = ta.ema(df["close"], 10), ta.ema(df["close"], 20)
buy = ta.crossover(fast, slow)

# valuewhen pulls the value of a series at the bar a condition last fired.
# n=1 = most recent buy, n=2 = the buy before that.
entry_price = ta.valuewhen(buy, df["close"], 1)
print("ta.valuewhen returns a", type(entry_price).__name__)

last_entry = float(np.asarray(entry_price)[-1])
now = df["close"].iloc[-1]
print(f"\nPrice at the last EMA buy cross: {last_entry:.2f}")
print(f"Current price                  : {now:.2f}")
print(f"Open trade P&L                 : {(now - last_entry) / last_entry * 100:+.2f}%")
print("\nvaluewhen is how a strategy remembers its entry to size stops and targets.")
```

Live output

```
ta.valuewhen returns a ndarray

Price at the last EMA buy cross: 784.90
Current price                  : 772.90
Open trade P&L                 : -1.53%

valuewhen is how a strategy remembers its entry to size stops and targets.
```

### rising and falling: stackable trend filters
Finally, **`rising(data, n)`**is True when a value is higher than it was`n` bars ago; **`falling`**is the opposite. They're simple, but combined with`&` they become powerful filters that demand multiple conditions at once. The example insists on _price rising AND volume rising_ together - a higher-quality up-move than price alone. Stacking filters like this is how you raise the bar for a signal.
EX 16rising and falling as confirmation filtersNSEch16/16_rising_falling.py
Copy
```
# rising / falling: simple trend filters you can stack onto any signal.
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
df = client.history(symbol="ICICIBANK", exchange="NSE", interval="D", start_date=start, end_date=end)

# rising/falling return NUMPY BOOLEAN ARRAYS: True if a value is higher/lower than n bars ago.
price_rising = ta.rising(df["close"], 3)
vol_rising = ta.rising(df["volume"], 3)
print("ta.rising returns a", type(price_rising).__name__, "of dtype", price_rising.dtype)

# Combine filters with & to demand both at once: a price up-move backed by rising volume.
confirmed = price_rising & vol_rising

print(f"\nBars where price has risen 3 sessions : {int(np.sum(price_rising))}")
print(f"Bars where BOTH price AND volume rising: {int(np.sum(confirmed))}")
print("Latest bar:", "confirmed up-move (price + volume)" if confirmed[-1]
      else "no confirmed up-move")
print(f"Price falling now? {bool(ta.falling(df['close'], 3)[-1])}")
```

Live output

```
ta.rising returns a ndarray of dtype bool

Bars where price has risen 3 sessions : 38
Bars where BOTH price AND volume rising: 19
Latest bar: no confirmed up-move
Price falling now? True
```

Tip
Because the utilities return NumPy boolean arrays, you combine them with `&` (and), `|` (or) and `~` (not) - not the Python keywords `and`/`or`. So `price_rising & vol_rising` works; `price_rising and vol_rising` will raise an error. This is the same vectorised-mask idea you met with NumPy in Chapter 6.
## Try it yourself
  * Build a two-condition entry: compute a 20-day `highest`, an `ADX`, and print only the days where price made a new 20-day high _and_ ADX was above 25 - a breakout filtered by trend strength.
  * Take the EMA crossover from the `crossover` example, clean it with `exrem`, convert it to a state with `flip`, and grab the entry price with `valuewhen`. You've just assembled the skeleton of a complete strategy.
  * Swap the correlation example's two stocks for a stock and a commodity (say a bank stock and `GOLDM03JUL26FUT` on MCX) and see how much weaker the correlation is across asset classes.


## Recap
  * **Statistical tools** treat price as data: regression and its **slope** read trend, **correlation** and **beta** measure relationships and market risk, **variance** measures spread, **TSF** projects one step ahead, and the **median** resists outliers.
  * **Hybrid indicators** combine ideas: **ADX** grades trend strength, **Aroon** its freshness, **pivot points** map support/resistance, **Parabolic SAR** trails a stop, **DMI** gives direction, and **fractals** mark swing points.
  * Always **check return types** : statistical/hybrid indicators give Series or tuples; we caught Parabolic SAR returning a Series, not a tuple.
  * The **utility helpers return NumPy arrays** and turn indicators into signals: `crossover`/`crossunder` mark the moment, `highest`/`lowest` define breakouts, `exrem` removes duplicates, `flip` builds a holding state, `valuewhen` remembers the entry, and `rising`/`falling` filter trend.
  * Combine boolean arrays with `&`, `|`, `~` - not `and`/`or` - and beware the look-ahead trap when testing breakouts.


With these utilities in hand you have the full vocabulary of signal-building. Next chapter we put them to work: taking raw indicators and forging them into clean, de-duplicated, look-ahead-safe entry and exit signals you can trust in a real backtest.
On this page
