Chapters
Module E · Strategy Playbook - Chapter 21
# Pair Trading & Statistical Arbitrage
Trade the spread: ratio, z-score, correlation and beta-neutral pairs.
NSE
What you'll learn
  * ·Build a price spread
  * ·Z-score of the spread
  * ·Correlation filter
  * ·Beta & hedge ratio
  * ·Entry/exit bands
  * ·Stat-arb mechanics


Every strategy so far has bet on _direction_ : this stock goes up, that future goes down. **Pair trading** does something cleverer - it bets on a _relationship_. You buy one stock and short another at the same time, and you profit when the gap between them behaves the way you expect, regardless of whether the whole market rises or falls. That last part is the magic word: **market-neutral**.
Here is the picture. Two banks like ICICIBANK and HDFCBANK are driven by the same forces - interest rates, the economy, banking news - so they tend to move together. Most days they rise and fall in lockstep. But every so often one runs ahead of the other for no good reason. Pair trading says: when they drift apart unusually far, bet that they snap back together. You go long the laggard and short the leader, and you win when the gap closes - even if both stocks crash, as long as the _spread_ between them reverts.
This is the gentle end of **statistical arbitrage** ("stat-arb"): using statistics, not gut feel, to find and trade these temporary dislocations. We'll build it piece by piece, and keep it didactic - every term defined, every number on screen.
Note
Pair trading needs two **correlated** instruments. We use two large private banks (ICICIBANK and HDFCBANK) as the main example and two public-sector banks (SBIN and BANKBARODA) as a second. All data is **daily** here, because the relationship plays out over days, not minutes.
## Step 1: line up the two legs
A pair has two **legs** - the two instruments you trade. The very first job is to download both price histories and align them on the same dates, so that row 100 is the same trading day for both. A pandas DataFrame built from two Series does this alignment automatically, and `.dropna()` throws away any date where one of them is missing.
EX 1Line up the two legs on the same datesNSEch21/01_two_legs.py
Copy
```
# Pair trading starts with two related stocks. We use ICICIBANK and HDFCBANK --
# two large private banks that tend to move together.
import os
import time
from datetime import datetime, timedelta

import pandas as pd

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=400)).strftime("%Y-%m-%d")


def closes(symbol):
    # Retry once -- a busy data server occasionally returns an error instead of a DataFrame.
    for _ in range(3):
        df = client.history(symbol=symbol, exchange="NSE", interval="D", start_date=start, end_date=end)
        if isinstance(df, pd.DataFrame) and "close" in df:
            return df["close"]
        time.sleep(1)
    raise RuntimeError(f"Could not fetch history for {symbol}: {df}")


# Line the two price series up on the same dates with a DataFrame.
pair = pd.DataFrame({"ICICIBANK": closes("ICICIBANK"), "HDFCBANK": closes("HDFCBANK")}).dropna()
print("Aligned daily closes:", len(pair), "rows")
print(pair.tail(5).round(2))
```

Live output

```
Aligned daily closes: 273 rows
            ICICIBANK  HDFCBANK
timestamp                      
2026-06-17     1336.8     787.1
2026-06-18     1342.3     799.0
2026-06-19     1346.5     779.8
2026-06-22     1352.4     786.4
2026-06-23     1335.5     772.9
```

You'll notice a small retry loop in the helper. A busy data server occasionally hands back an error instead of a table; retrying once or twice makes the example robust. It is a good habit for any script that fetches lots of data.
## Step 2: the correlation filter
Before trading a pair, you must confirm the two legs _actually_ move together. The tool is **correlation** - a single number from -1 to +1. A correlation near +1 means they rise and fall together; near 0 means they are unrelated; near -1 means they move opposite. We measure it on **daily returns** , not raw prices, because two rising stocks can look correlated just from a shared uptrend even if their day-to-day wiggles are unrelated.
EX 2Confirm the pair moves togetherNSEch21/02_correlation.py
Copy
```
# Correlation filter: only trade a pair whose two legs actually move together.
import os
import time
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=400)).strftime("%Y-%m-%d")


def closes(symbol):
    for _ in range(3):
        df = client.history(symbol=symbol, exchange="NSE", interval="D",
                            start_date=start, end_date=end)
        if isinstance(df, pd.DataFrame) and "close" in df:
            return df["close"]
        time.sleep(1)
    raise RuntimeError(f"Could not fetch history for {symbol}: {df}")


pair = pd.DataFrame({"ICICIBANK": closes("ICICIBANK"), "HDFCBANK": closes("HDFCBANK")}).dropna()

# Correlation of DAILY RETURNS (not raw prices) is what matters for a pair.
rets = pair.pct_change().dropna()
corr = np.corrcoef(rets["ICICIBANK"], rets["HDFCBANK"])[0, 1]

print(f"Daily-return correlation: {corr:.3f}")
if corr > 0.6:
    print("Strong positive correlation -- a sensible pair to trade.")
else:
    print("Weak correlation -- skip this pair, the spread will not behave predictably.")
```

Live output

```
Daily-return correlation: 0.601
Strong positive correlation -- a sensible pair to trade.
```

Heads up
Correlation is a _filter_ , not a guarantee. A correlation of 0.6 today can decay to 0.2 next quarter if one company's story changes - a merger, a scandal, a regulatory hit. A pair only works while the economic link that binds the two stocks holds. We'll watch this with a rolling correlation later in the chapter.
## Step 3: build the spread
The **spread** is the thing you actually trade - a single number that captures the relationship between the two legs. The simplest spread is the **price ratio** : leg A's price divided by leg B's. For a stable pair this ratio drifts around a fairly constant level. When the ratio is high, A is expensive relative to B; when it's low, A is cheap relative to B.
EX 3Build the price ratio (the spread)NSEch21/03_ratio_spread.py
Copy
```
# The price ratio: the simplest "spread" between two stocks.
import os
import time
from datetime import datetime, timedelta

import pandas as pd

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=400)).strftime("%Y-%m-%d")


def closes(symbol):
    for _ in range(3):
        df = client.history(symbol=symbol, exchange="NSE", interval="D",
                            start_date=start, end_date=end)
        if isinstance(df, pd.DataFrame) and "close" in df:
            return df["close"]
        time.sleep(1)
    raise RuntimeError(f"Could not fetch history for {symbol}: {df}")


pair = pd.DataFrame({"ICICIBANK": closes("ICICIBANK"), "HDFCBANK": closes("HDFCBANK")}).dropna()

# Ratio = price of leg A divided by price of leg B. For a stable pair this ratio
# wanders around a fairly constant level and is the thing we actually trade.
pair["ratio"] = pair["ICICIBANK"] / pair["HDFCBANK"]

print("Price ratio ICICIBANK / HDFCBANK:")
print(pair[["ICICIBANK", "HDFCBANK", "ratio"]].tail(5).round(3))
print(f"\nRatio mean over the window: {pair['ratio'].mean():.3f}")
print(f"Ratio min / max:            {pair['ratio'].min():.3f} / {pair['ratio'].max():.3f}")
```

Live output

```
Price ratio ICICIBANK / HDFCBANK:
            ICICIBANK  HDFCBANK  ratio
timestamp                             
2026-06-17     1336.8     787.1  1.698
2026-06-18     1342.3     799.0  1.680
2026-06-19     1346.5     779.8  1.727
2026-06-22     1352.4     786.4  1.720
2026-06-23     1335.5     772.9  1.728

Ratio mean over the window: 1.496
Ratio min / max:            1.341 / 1.769
```

## Step 4: the z-score
A raw ratio of, say, 0.74 means nothing on its own - is that high or low? To judge it we need context, and that's what the **z-score** gives. The z-score answers: _how many standard deviations is the ratio away from its recent average?_ We compute a **rolling mean** and **rolling standard deviation** (the typical wiggle) over a window - 30 days here - then:

```
z = (ratio - rolling_mean) / rolling_std

```

A z-score of 0 means the ratio is dead-on average. +2 means it's stretched two standard deviations high (A unusually expensive vs B); -2 means stretched two low (A unusually cheap). Extreme z-scores are our trade triggers.
EX 4Z-score of the spreadNSEch21/04_zscore.py
Copy
```
# Z-score of the spread: how many standard deviations is the ratio from "normal"?
import os
import time
from datetime import datetime, timedelta

import pandas as pd

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=400)).strftime("%Y-%m-%d")


def closes(symbol):
    for _ in range(3):
        df = client.history(symbol=symbol, exchange="NSE", interval="D",
                            start_date=start, end_date=end)
        if isinstance(df, pd.DataFrame) and "close" in df:
            return df["close"]
        time.sleep(1)
    raise RuntimeError(f"Could not fetch history for {symbol}: {df}")


pair = pd.DataFrame({"ICICIBANK": closes("ICICIBANK"), "HDFCBANK": closes("HDFCBANK")}).dropna()
pair["ratio"] = pair["ICICIBANK"] / pair["HDFCBANK"]

# Rolling mean and standard deviation over a 30-day window define "normal".
window = 30
pair["mean"] = pair["ratio"].rolling(window).mean()
pair["std"] = pair["ratio"].rolling(window).std()
# Z-score = (value - mean) / std. Zero means dead-on average; +2 means stretched high.
pair["zscore"] = (pair["ratio"] - pair["mean"]) / pair["std"]

print(pair[["ratio", "mean", "zscore"]].dropna().tail(6).round(3))
z = pair["zscore"].iloc[-1]
print(f"\nLatest z-score: {z:.2f}  -- the spread is {abs(z):.1f} std devs",
      "above" if z > 0 else "below", "its 30-day mean.")
```

Live output

```
ratio   mean  zscore
timestamp                       
2026-06-16  1.700  1.661   0.918
2026-06-17  1.698  1.664   0.823
2026-06-18  1.680  1.666   0.335
2026-06-19  1.727  1.670   1.397
2026-06-22  1.720  1.674   1.147
2026-06-23  1.728  1.676   1.259

Latest z-score: 1.26  -- the spread is 1.3 std devs above its 30-day mean.
```

## Step 5: entry and exit bands
Now the rules write themselves. The classic bands are **enter at |z| > 2, exit near z = 0**:
  * **z > +2** - the ratio is too high. We expect it to fall back, so we **short the spread** : sell leg A, buy leg B.
  * **z < -2** - the ratio is too low. We expect it to rise, so we **go long the spread** : buy leg A, sell leg B.
  * **|z| < 0.5** - the spread is back to normal. Close the trade and take the profit.

EX 5Entry and exit bands on the z-scoreNSEch21/05_entry_exit_bands.py
Copy
```
# Entry/exit bands: enter when |z| > 2, exit when the spread returns near 0.
import os
import time
from datetime import datetime, timedelta

import pandas as pd

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=400)).strftime("%Y-%m-%d")


def closes(symbol):
    for _ in range(3):
        df = client.history(symbol=symbol, exchange="NSE", interval="D",
                            start_date=start, end_date=end)
        if isinstance(df, pd.DataFrame) and "close" in df:
            return df["close"]
        time.sleep(1)
    raise RuntimeError(f"Could not fetch history for {symbol}: {df}")


pair = pd.DataFrame({"ICICIBANK": closes("ICICIBANK"), "HDFCBANK": closes("HDFCBANK")}).dropna()
pair["ratio"] = pair["ICICIBANK"] / pair["HDFCBANK"]
pair["z"] = (pair["ratio"] - pair["ratio"].rolling(30).mean()) / pair["ratio"].rolling(30).std()

# The trading rules, as plain English -> code:
#   z > +2  : ratio too HIGH -> SELL ICICIBANK, BUY HDFCBANK (bet it falls back)
#   z < -2  : ratio too LOW  -> BUY ICICIBANK, SELL HDFCBANK (bet it rises back)
#   |z| < 0.5: spread back to normal -> close the trade.
pair["signal"] = "flat"
pair.loc[pair["z"] > 2, "signal"] = "short_spread"
pair.loc[pair["z"] < -2, "signal"] = "long_spread"
pair.loc[pair["z"].abs() < 0.5, "signal"] = "exit"

events = pair[pair["signal"] != "flat"][["ratio", "z", "signal"]].dropna()
print("Recent band events (entries and exits):")
print(events.tail(8).round(3))
```

Live output

```
Recent band events (entries and exits):
            ratio      z        signal
timestamp                             
2026-05-26  1.642 -0.345          exit
2026-06-02  1.639 -0.381          exit
2026-06-03  1.648 -0.049          exit
2026-06-04  1.660  0.427          exit
2026-06-09  1.727  2.897  short_spread
2026-06-10  1.732  2.617  short_spread
2026-06-11  1.769  3.019  short_spread
2026-06-18  1.680  0.335          exit
```

Tip
Notice the trade is symmetric: whichever way the spread is stretched, you bet on the _return to normal_ , not on a direction. That symmetry is why pair trading can make money in up markets, down markets and flat markets - it only needs the gap to close.
## Step 6: the hedge ratio (beta)
So far we've assumed one share of A balances one share of B. That's rarely true - if A trades at 1,400 and B at 1,000, a one-for-one trade is lopsided and exposed to the market. The **hedge ratio** (also called **beta**) fixes this: it's the number of units of B that best offsets one unit of A, found by a simple linear regression of A's price on B's. A beta-weighted spread (`A - beta * B`) is more stable and more truly market-neutral than a raw ratio.
EX 6Beta and the hedge ratioNSEch21/06_hedge_ratio.py
Copy
```
# Beta / hedge ratio: how many shares of leg B balance one share of leg A.
import os
import time
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=400)).strftime("%Y-%m-%d")


def closes(symbol):
    for _ in range(3):
        df = client.history(symbol=symbol, exchange="NSE", interval="D",
                            start_date=start, end_date=end)
        if isinstance(df, pd.DataFrame) and "close" in df:
            return df["close"]
        time.sleep(1)
    raise RuntimeError(f"Could not fetch history for {symbol}: {df}")


a = closes("ICICIBANK")
b = closes("HDFCBANK")
pair = pd.DataFrame({"a": a, "b": b}).dropna()

# Hedge ratio (beta) = slope of a regression of A's price on B's price.
# polyfit(x, y, 1) returns [slope, intercept].
beta, intercept = np.polyfit(pair["b"], pair["a"], 1)
print(f"Hedge ratio (beta): {beta:.3f}")
print(f"Meaning: to be market-neutral, hold ~{beta:.2f} units of HDFCBANK for every 1 of ICICIBANK.")

# A beta-weighted spread is more stable than a raw price difference.
pair["spread"] = pair["a"] - beta * pair["b"]
print(f"\nBeta-neutral spread -- mean {pair['spread'].mean():.2f}, std {pair['spread'].std():.2f}")
print(pair[["spread"]].tail(4).round(2))
```

Live output

```
Hedge ratio (beta): 0.597
Meaning: to be market-neutral, hold ~0.60 units of HDFCBANK for every 1 of ICICIBANK.

Beta-neutral spread -- mean 820.89, std 37.96
            spread
timestamp         
2026-06-18  865.60
2026-06-19  881.26
2026-06-22  883.22
2026-06-23  874.38
```

This beta is the heart of **market-neutral mechanics**. By holding the two legs in beta-proportion, the broad market moves cancel out: if the whole market jumps 2%, your long leg gains and your short leg loses by roughly the same amount, leaving you exposed only to the _spread_ - exactly the bet you wanted to make.
## Step 7: watch the correlation decay
Correlation is not fixed. A pair that was tight last year can come apart, and the moment it does, the spread stops reverting and your strategy starts bleeding. So we track a **rolling correlation** through time using `ta.correlation`, and we stand aside whenever it collapses.
EX 7Track rolling correlation over timeNSEch21/07_rolling_correl.py
Copy
```
# Correlation is not constant -- track it with a rolling window using ta.correlation.
import os
import time
from datetime import datetime, timedelta

import pandas as pd

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=400)).strftime("%Y-%m-%d")


def closes(symbol):
    for _ in range(3):
        df = client.history(symbol=symbol, exchange="NSE", interval="D",
                            start_date=start, end_date=end)
        if isinstance(df, pd.DataFrame) and "close" in df:
            return df["close"]
        time.sleep(1)
    raise RuntimeError(f"Could not fetch history for {symbol}: {df}")


pair = pd.DataFrame({"ICICIBANK": closes("ICICIBANK"), "HDFCBANK": closes("HDFCBANK")}).dropna()

# Correlate DAILY RETURNS (not raw prices) -- same rule as the static filter earlier.
rets = pair.pct_change().dropna()
# ta.correlation gives a rolling Pearson correlation between two series.
pair["correl_30"] = ta.correlation(rets["ICICIBANK"], rets["HDFCBANK"], 30)

recent = pair["correl_30"].dropna()
print("Rolling 30-day return correlation:")
print(recent.tail(6).round(3))
print(f"\nLowest it dropped to: {recent.min():.3f}")
print("When rolling correlation collapses, the pair has 'broken' -- stand aside until it recovers.")
```

Live output

```
Rolling 30-day return correlation:
timestamp
2026-06-16    0.668
2026-06-17    0.664
2026-06-18    0.616
2026-06-19    0.582
2026-06-22    0.561
2026-06-23    0.603
Name: correl_30, dtype: float64

Lowest it dropped to: -0.097
When rolling correlation collapses, the pair has 'broken' -- stand aside until it recovers.
```

## A second pair, same recipe
The whole framework is reusable. Swap in two public-sector banks - SBIN and BANKBARODA - and run the identical steps: check correlation, build the ratio, compute the z-score. The point is that nothing about the method is specific to one pair; the discipline of re-checking correlation every time is what keeps you out of broken pairs.
EX 8The same recipe on a second pairNSEch21/08_second_pair.py
Copy
```
# A second pair from the public-sector banks: SBIN and BANKBARODA.
import os
import time
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=400)).strftime("%Y-%m-%d")


def closes(symbol):
    for _ in range(3):
        df = client.history(symbol=symbol, exchange="NSE", interval="D",
                            start_date=start, end_date=end)
        if isinstance(df, pd.DataFrame) and "close" in df:
            return df["close"]
        time.sleep(1)
    raise RuntimeError(f"Could not fetch history for {symbol}: {df}")


pair = pd.DataFrame({"SBIN": closes("SBIN"), "BANKBARODA": closes("BANKBARODA")}).dropna()
pair["ratio"] = pair["SBIN"] / pair["BANKBARODA"]
pair["z"] = (pair["ratio"] - pair["ratio"].rolling(30).mean()) / pair["ratio"].rolling(30).std()

rets = pair[["SBIN", "BANKBARODA"]].pct_change().dropna()
corr = np.corrcoef(rets["SBIN"], rets["BANKBARODA"])[0, 1]

print(f"SBIN / BANKBARODA return correlation: {corr:.3f}")
print(f"Current ratio: {pair['ratio'].iloc[-1]:.3f}   z-score: {pair['z'].iloc[-1]:.2f}")
print("\nSame recipe, different pair. Always re-check correlation -- not every duo behaves.")
```

Live output

```
SBIN / BANKBARODA return correlation: 0.653
Current ratio: 3.687   z-score: -0.66

Same recipe, different pair. Always re-check correlation -- not every duo behaves.
```

## Backtesting the spread trade
Finally, let's test the z-score rules with **VectorBT**. To keep the demo readable we trade just the ICICIBANK leg, going long when the spread is stretched low and short when it's stretched high - the same z-score signal a full two-leg trade would use. VectorBT's `from_signals` accepts separate `entries`/`exits` for longs and `short_entries`/`short_exits` for shorts, which maps neatly onto our bands.
EX 9Backtest the z-score pair tradeNSEch21/09_pair_backtest.py
Copy
```
# Backtest the z-score pair trade on the ICICIBANK leg with VectorBT.
import os
import time
from datetime import datetime, timedelta

import pandas as pd

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=400)).strftime("%Y-%m-%d")


def closes(symbol):
    for _ in range(3):
        df = client.history(symbol=symbol, exchange="NSE", interval="D",
                            start_date=start, end_date=end)
        if isinstance(df, pd.DataFrame) and "close" in df:
            return df["close"]
        time.sleep(1)
    raise RuntimeError(f"Could not fetch history for {symbol}: {df}")


pair = pd.DataFrame({"ICICIBANK": closes("ICICIBANK"), "HDFCBANK": closes("HDFCBANK")}).dropna()
pair["ratio"] = pair["ICICIBANK"] / pair["HDFCBANK"]
pair["z"] = (pair["ratio"] - pair["ratio"].rolling(30).mean()) / pair["ratio"].rolling(30).std()

# We trade only the ICICIBANK leg here to keep the demo simple; a real pair trade also
# shorts HDFCBANK, but the z-score signal is identical. z<-2: cheap -> long, exit near 0.
# z>+2: rich -> short, cover near 0.
long_entries = pair["z"] < -2
long_exits = pair["z"] > -0.5
short_entries = pair["z"] > 2
short_exits = pair["z"] < 0.5

import vectorbt as vbt

pf = vbt.Portfolio.from_signals(pair["ICICIBANK"], entries=long_entries, exits=long_exits,
                                short_entries=short_entries, short_exits=short_exits,
                                init_cash=200000, fees=0.001, freq="1D")
print("Z-score reversion on ICICIBANK leg (entry |z|>2, exit near 0)")
print("Trades       :", int(pf.trades.count()))
print("Total return :", round(float(pf.total_return()) * 100, 2), "%")
print("\nMarket-neutral: the matching HDFCBANK short leg would cancel most market risk,")
print("so you profit from the SPREAD closing -- not from the market's direction.")
```

Live output

```
Z-score reversion on ICICIBANK leg (entry |z|>2, exit near 0)
Trades       : 6
Total return : -3.18 %

Market-neutral: the matching HDFCBANK short leg would cancel most market risk,
so you profit from the SPREAD closing -- not from the market's direction.
```

Heads up
A single-leg backtest _overstates_ a pair trade's risk, because in reality the matching short leg cancels most of the market swings. But it also flatters it in another way: real pair trades pay **two sets of costs** (you trade both legs) and shorting carries borrow fees and the risk of a short squeeze. Pair trading is elegant, but it is not free money - the spread can stay irrational longer than your capital lasts.
## Try it yourself
  * Change the z-score entry band in `05_entry_exit_bands.py` from 2.0 to 2.5. Fewer, higher-conviction trades - does the backtest improve?
  * Try a different rolling window for the mean and std (e.g. 20 or 60 days) and watch how the z-score becomes jumpier or smoother.
  * Pick your own pair - two cement makers, two IT majors - and run `02_correlation.py` on it. Is the correlation high enough to bother?


## Recap
  * **Pair trading** bets on the _relationship_ between two correlated instruments, not on market direction - it is **market-neutral**.
  * A **correlation filter** (on daily returns) confirms the two legs move together before you trade them.
  * The **spread** - a price ratio or a beta-weighted difference - is the single series you actually trade.
  * The **z-score** measures how stretched the spread is; the classic rule is enter at **|z| > 2**, exit near **0**.
  * The **hedge ratio (beta)** sizes the two legs so the market cancels out, leaving only the spread exposed.
  * Correlation **decays** - track it with a rolling window and stand aside when a pair breaks.


Next we turn to two of the most studied forces in markets - momentum and volatility - and use them to rank stocks, time breakouts, and size positions by risk.
On this page
