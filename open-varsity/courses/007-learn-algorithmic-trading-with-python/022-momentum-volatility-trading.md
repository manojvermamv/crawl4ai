Chapters
Module E · Strategy Playbook - Chapter 22
# Momentum & Volatility Trading
Cross-sectional momentum plus ATR / Bollinger volatility-driven entries and sizing.
NSEMCX
What you'll learn
  * ·Cross-sectional momentum
  * ·ATR breakout
  * ·Bollinger squeeze
  * ·Volatility targeting
  * ·Regime filter
  * ·Vol-scaled position size


Two forces show up again and again in serious quantitative trading: **momentum** and **volatility**. Momentum is the well-documented tendency for what has been going up to keep going up - winners keep winning, for a while. Volatility is how much an instrument jumps around, and it's the key to _risk_ : how big a position you can safely hold, and where a breakout really begins. This chapter weaves the two together.
We'll do four things. First, **cross-sectional momentum** - rank a basket of stocks against each other and hold the strongest. Second, an **ATR breakout** - enter when price clears a volatility-sized hurdle. Third, the **Bollinger squeeze** - spot quiet coils that precede big moves. Fourth, **volatility targeting** - size positions so that a calm stock and a wild one contribute the same risk. And tying it together, a **regime filter** that only lets us go long when the broader trend is up.
Note
We work mostly with **daily** data across a small universe of NSE stocks, and finish with an **MCX** commodity (mini gold) to show the same volatility tools work on any market. Run each example with `uv run python the_file.py`.
## Building a universe
Cross-sectional momentum compares stocks _against each other_ , so first we need several of them lined up in one table. We download daily closes for eight liquid NSE names and assemble a **panel** : dates down the rows, stocks across the columns. The small retry loop guards against the occasional busy-server hiccup when fetching many symbols in a row.
EX 1Build an 8-stock universeNSEch22/01_universe.py
Copy
```
# Build a small universe of 8 NSE stocks and download their daily closes.
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

universe = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "SBIN", "HINDUNILVR", "ITC"]


def closes(symbol):
    # Retry -- fetching many symbols in a loop can hit a busy data server.
    for _ in range(3):
        df = client.history(symbol=symbol, exchange="NSE", interval="D",
                            start_date=start, end_date=end)
        if isinstance(df, pd.DataFrame) and "close" in df:
            return df["close"]
        time.sleep(1)
    raise RuntimeError(f"Could not fetch history for {symbol}: {df}")


# One tidy table: dates down the rows, stocks across the columns.
panel = pd.DataFrame({symbol: closes(symbol) for symbol in universe}).dropna()
print("Universe:", len(universe), "stocks,", len(panel), "common trading days")
print(panel.tail(3).round(1))
```

Live output

```
Universe: 8 stocks, 273 common trading days
            RELIANCE     TCS    INFY  ...    SBIN  HINDUNILVR    ITC
timestamp                             ...                           
2026-06-19    1309.5  2125.0  1051.4  ...  1035.1      2194.6  292.5
2026-06-22    1326.5  2127.8  1065.4  ...  1040.8      2184.9  291.2
2026-06-23    1306.0  2060.0  1029.0  ...  1023.6      2160.0  290.0

[3 rows x 8 columns]
```

## Cross-sectional momentum
The idea is delightfully simple: measure each stock's return over the last 60 trading days, rank them from best to worst, and **buy the top few**. "Cross-sectional" means we judge each stock _relative to its peers_ on the same day - not against its own history. The leaders today have momentum; we ride them and rebalance periodically.
EX 2Rank by 60-day return, buy the leadersNSEch22/02_cross_sectional_momentum.py
Copy
```
# Cross-sectional momentum: rank the universe by 60-day return, buy the leaders.
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

universe = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "SBIN", "HINDUNILVR", "ITC"]


def closes(symbol):
    for _ in range(3):
        df = client.history(symbol=symbol, exchange="NSE", interval="D",
                            start_date=start, end_date=end)
        if isinstance(df, pd.DataFrame) and "close" in df:
            return df["close"]
        time.sleep(1)
    raise RuntimeError(f"Could not fetch history for {symbol}: {df}")


panel = pd.DataFrame({s: closes(s) for s in universe}).dropna()

# 60-day return for every stock, then sort high to low.
momentum = panel.pct_change(60).iloc[-1].sort_values(ascending=False) * 100

print("60-day return ranking (%):")
print(momentum.round(2).to_string())

top_n = 3
winners = list(momentum.head(top_n).index)
print(f"\nGo long the top {top_n}: {winners}")
print("'Cross-sectional' means we compare stocks AGAINST EACH OTHER, then hold the strongest.")
```

Live output

```
60-day return ranking (%):
ICICIBANK      9.23
HINDUNILVR     5.25
HDFCBANK       3.86
ITC            2.56
SBIN          -0.80
RELIANCE      -7.23
TCS          -13.58
INFY         -16.36

Go long the top 3: ['ICICIBANK', 'HINDUNILVR', 'HDFCBANK']
'Cross-sectional' means we compare stocks AGAINST EACH OTHER, then hold the strongest.
```

Tip
Why 60 days? Momentum research consistently finds the effect is strongest over a few months - long enough to capture a real trend, short enough to still be timely. A common refinement is to skip the most recent week (the "12-1" idea) because the very latest move often reverses. Start with a plain lookback, then experiment.
## Measuring volatility with ATR
To trade volatility you must first measure it. **ATR** - Average True Range - is the cleanest gauge: it averages the daily _true range_ (today's high-to-low, adjusted for gaps) over 14 days, giving you a single number in rupees that says "this is how much this stock typically moves in a day." Expressed as a percentage of price, it lets you compare a 3,000-rupee stock with a 200-rupee one fairly.
EX 3ATR: how much a stock moves per dayNSEch22/03_atr.py
Copy
```
# ATR (Average True Range): a clean dollar measure of how much a stock moves per day.
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

# ATR averages the true range (today's range, accounting for gaps) over 14 days.
df["atr"] = ta.atr(df["high"], df["low"], df["close"], period=14)
df["atr_pct"] = df["atr"] / df["close"] * 100

print(df[["close", "atr", "atr_pct"]].tail(5).round(2))
last = df.iloc[-1]
print(f"\nRELIANCE typically moves about Rs {last['atr']:.1f} a day ({last['atr_pct']:.2f}% of price).")
print("ATR is the building block for both breakout levels and position sizing.")
```

Live output

```
close    atr  atr_pct
timestamp                         
2026-06-17  1332.7  27.43     2.06
2026-06-18  1328.1  26.32     1.98
2026-06-19  1309.5  26.79     2.05
2026-06-22  1326.5  27.40     2.07
2026-06-23  1306.0  27.52     2.11

RELIANCE typically moves about Rs 27.5 a day (2.11% of price).
ATR is the building block for both breakout levels and position sizing.
```

## ATR breakout entry
Now we use ATR as a _hurdle_. A naive breakout buys when price makes a new high - but a new high by one paisa is just noise. An **ATR breakout** demands a move of real size: buy only when price closes above the _previous_ close plus, say, one ATR. Because the hurdle scales with each stock's own volatility, the same rule works on a sleepy stock and a jumpy one.
Notice the `.shift(1)` on both the close and the ATR - that's how we avoid **look-ahead bias** , the cardinal sin of backtesting. We only ever use information that was known _before_ today's bar formed.
EX 4An ATR-sized breakout entryNSEch22/04_atr_breakout.py
Copy
```
# ATR breakout entry: buy when price closes above yesterday's close + N x ATR.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=200)).strftime("%Y-%m-%d")
df = client.history(symbol="ICICIBANK", exchange="NSE", interval="D", start_date=start, end_date=end)

df["atr"] = ta.atr(df["high"], df["low"], df["close"], period=14)

# The breakout level sits one ATR above the PREVIOUS close. .shift(1) avoids look-ahead:
# we only use information that was known before today's bar formed.
mult = 1.0
df["trigger"] = df["close"].shift(1) + mult * df["atr"].shift(1)
df["breakout"] = df["close"] > df["trigger"]

signals = df[df["breakout"]][["close", "trigger"]].dropna()
print(f"Breakout days (close > prev close + {mult} ATR):", len(signals))
print(signals.tail(5).round(2))
print("\nSizing the trigger in ATRs adapts the strategy to each stock's own volatility.")
```

Live output

```
Breakout days (close > prev close + 1.0 ATR): 9
             close  trigger
timestamp                  
2026-02-03  1389.7  1379.10
2026-03-10  1311.9  1307.14
2026-04-08  1309.2  1275.86
2026-04-10  1321.9  1315.69
2026-05-25  1291.8  1289.07

Sizing the trigger in ATRs adapts the strategy to each stock's own volatility.
```

Heads up
**Look-ahead bias** is the silent killer of backtests. If your entry rule peeks at today's high or close to decide today's trade, your results will look spectacular and be completely fake - you can't trade on information you didn't have yet. Shift any indicator you use for a decision back by one bar, every time.
## The Bollinger squeeze
**Bollinger Bands** wrap a moving average in an envelope set two standard deviations wide. When volatility is low the bands pinch together; when it's high they balloon out. The **squeeze** is that pinch - a quiet, coiled market that historically precedes a sharp expansion. We measure the pinch with **bandwidth** (`ta.bbwidth`): when bandwidth drops into the bottom fifth of its recent range, the market is squeezed and we get ready for a breakout.
EX 5Spot a Bollinger squeezeNSEch22/05_bollinger_squeeze.py
Copy
```
# Bollinger squeeze: spot low-volatility coils, then trade the expansion.
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

# Bandwidth = how wide the Bollinger Bands are. Low bandwidth = a quiet "squeeze";
# the band then expands when a move finally breaks out.
df["bbwidth"] = ta.bbwidth(df["close"], period=20, std_dev=2.0)

# A squeeze: bandwidth in the bottom 20% of its recent range.
floor = df["bbwidth"].rolling(60).quantile(0.20)
df["squeeze"] = df["bbwidth"] < floor

print(df[["close", "bbwidth", "squeeze"]].dropna().tail(6).round(4))
print("\nSqueeze days in the window:", int(df["squeeze"].sum()))
print("Quiet bands tend to precede big moves -- arm a breakout order when a squeeze appears.")
```

Live output

```
close  bbwidth  squeeze
timestamp                           
2026-06-16  2199.0   0.1443    False
2026-06-17  2223.0   0.1412    False
2026-06-18  2203.3   0.1380    False
2026-06-19  2125.0   0.1400    False
2026-06-22  2127.8   0.1405    False
2026-06-23  2060.0   0.1489    False

Squeeze days in the window: 11
Quiet bands tend to precede big moves -- arm a breakout order when a squeeze appears.
```

The squeeze tells you _when_ a move is likely, not _which way_. Traders pair it with a directional trigger - often the very ATR breakout above - so the squeeze arms the trade and the breakout fires it.
## The regime filter
Momentum has a dark side: it loves to buy right before a crash, because a falling market briefly produces strong-looking "winners" on the way down. The cure is a **regime filter** : a coarse on/off switch that only allows long trades when the broader trend is healthy. The standard one is the **200-day SMA** - if price is above its 200-day simple moving average, we're in a bull regime and longs are allowed; below it, we stand aside.
EX 6Only go long above the 200-day SMANSEch22/06_regime_filter.py
Copy
```
# Regime filter: only take long trades when price is above its 200-day SMA.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=500)).strftime("%Y-%m-%d")
df = client.history(symbol="HDFCBANK", exchange="NSE", interval="D", start_date=start, end_date=end)

# The 200-day SMA is the classic line between a bull and a bear regime.
df["sma200"] = ta.sma(df["close"], 200)
df["bull"] = df["close"] > df["sma200"]

last = df.dropna().iloc[-1]
in_uptrend = bool(last["bull"])
bull_days = int(df["bull"].sum())

print(f"Close {last['close']:.1f}  vs 200-SMA {last['sma200']:.1f}")
print("Regime now:", "UPTREND -- longs allowed" if in_uptrend else "DOWNTREND -- stand aside")
print(f"Days in uptrend over the window: {bull_days} of {df['bull'].notna().sum()}")
print("\nA regime filter keeps you from buying momentum into a falling market -- the No.1 way these systems blow up.")
```

Live output

```
Close 772.9  vs 200-SMA 898.8
Regime now: DOWNTREND -- stand aside
Days in uptrend over the window: 24 of 336

A regime filter keeps you from buying momentum into a falling market -- the No.1 way these systems blow up.
```

## Volatility targeting: sizing by risk
Here is one of the most powerful ideas in the whole series. A fixed position size is a trap: 100 shares of a calm stock and 100 shares of a wild one carry wildly different risk. **Volatility targeting** fixes this by sizing each position so they all contribute the _same_ risk:

```
position_size = target_vol / realised_vol

```

We pick a target - say 15% annualised volatility for the position - and measure each instrument's **realised volatility** (the annualised standard deviation of its recent daily returns). A calm stock (low realised vol) gets a _bigger_ position; a stormy one gets a _smaller_ position. The result is risk that stays roughly constant whether markets are sleepy or panicking. We cap the size to avoid dangerous leverage when vol is unusually low.
EX 7Size positions by volatilityNSEch22/07_vol_targeting.py
Copy
```
# Volatility targeting: size each position by target_vol / realised_vol.
import os
from datetime import datetime, timedelta

import numpy as np

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=200)).strftime("%Y-%m-%d")
df = client.history(symbol="SBIN", exchange="NSE", interval="D", start_date=start, end_date=end)

# Realised vol = annualised std dev of daily returns over 20 days.
daily_ret = df["close"].pct_change()
realised_vol = daily_ret.rolling(20).std() * np.sqrt(252)

# Aim for a steady 15% portfolio volatility. Quiet stock -> bigger position; wild stock -> smaller.
target_vol = 0.15
raw_size = target_vol / realised_vol
position = raw_size.clip(upper=3.0)  # cap leverage at 3x for safety

capital = 200000
last_price = df["close"].iloc[-1]
shares = int((capital * position.iloc[-1]) / last_price)

print(f"Realised volatility: {realised_vol.iloc[-1] * 100:.1f}%   target: {target_vol * 100:.0f}%")
print(f"Volatility-scaled size factor: {position.iloc[-1]:.2f}x")
print(f"At Rs {last_price:.1f}, that is about {shares} shares on Rs {capital:,} capital.")
print("\nVol targeting keeps risk roughly CONSTANT across calm and stormy markets.")
```

Live output

```
Realised volatility: 15.4%   target: 15%
Volatility-scaled size factor: 0.97x
At Rs 1023.6, that is about 190 shares on Rs 200,000 capital.

Vol targeting keeps risk roughly CONSTANT across calm and stormy markets.
```

Key idea
Volatility targeting is what professional managers mean by "risk parity" at the single-position level. It turns "how many shares?" from a guess into a calculation, and it's the single biggest upgrade most discretionary traders can make to their sizing. Keep the leverage cap - without it, a freakishly quiet stock can size you into a position that destroys you the moment vol returns.
## The same tools on a commodity
None of this is specific to equities. Volatility lives in every market, and ATR adapts automatically. Here we run the ATR breakout on **mini gold (GOLDM) on MCX** - a commodity future with its own rhythm and its own volatility. The code is identical; only the symbol and exchange change.
EX 8ATR breakout on MCX goldMCXch22/08_mcx_atr_breakout.py
Copy
```
# The same volatility toolkit on a commodity: an ATR breakout on MCX gold.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=300)).strftime("%Y-%m-%d")
# GOLDM = the mini gold future on MCX, a popular commodity for volatility strategies.
df = client.history(symbol="GOLDM03JUL26FUT", exchange="MCX", interval="D", start_date=start, end_date=end)

df["atr"] = ta.atr(df["high"], df["low"], df["close"], period=14)
df["trigger"] = df["close"].shift(1) + 1.5 * df["atr"].shift(1)
df["breakout"] = df["close"] > df["trigger"]

last = df.iloc[-1]
print(f"GOLDM close {last['close']:.0f}   ATR {last['atr']:.0f}   ({last['atr'] / last['close'] * 100:.2f}% of price)")
print("Breakout days in window:", int(df["breakout"].sum()))
print(df[df["breakout"]][["close", "trigger"]].dropna().tail(4).round(0))
print("\nCommodities like gold and crude carry their own volatility -- ATR adapts automatically.")
```

Live output

```
GOLDM close 144280   ATR 2835   (1.96% of price)
Breakout days in window: 4
             close   trigger
timestamp                   
2026-01-27  183027  181990.0
2026-01-28  191576  188723.0
2026-01-29  198661  197881.0
2026-05-13  163824  158990.0

Commodities like gold and crude carry their own volatility -- ATR adapts automatically.
```

## Putting it together: a backtest
Finally we combine momentum _and_ the regime filter and test it in **VectorBT**. We go long the strongest stock from our universe only when its 60-day momentum is positive **and** price is above its 200-day SMA, and we exit when either condition fails. The regime filter is the part that earns its keep - it's what stops momentum from buying into a falling market.
EX 9Backtest regime-filtered momentumNSEch22/09_momentum_backtest.py
Copy
```
# Backtest a regime-filtered momentum trade on the strongest stock with VectorBT.
import os
from datetime import datetime, timedelta

import pandas as pd

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=500)).strftime("%Y-%m-%d")
# ICICIBANK led the 60-day momentum ranking earlier -- backtest a trend trade on it.
df = client.history(symbol="ICICIBANK", exchange="NSE", interval="D", start_date=start, end_date=end)

close = df["close"]
mom = close.pct_change(60)            # positive momentum = an uptrend
sma200 = ta.sma(close, 200)           # regime filter
bull = close > sma200

# Enter long only when BOTH momentum is positive AND we are in a bull regime.
entries = (mom > 0) & bull & ~((mom.shift(1) > 0) & bull.shift(1))
exits = (mom < 0) | ~bull

import vectorbt as vbt

pf = vbt.Portfolio.from_signals(close, entries.fillna(False), exits.fillna(False),
                                init_cash=200000, fees=0.001, freq="1D")
print("Momentum + 200-SMA regime filter on ICICIBANK")
print("Total return :", round(float(pf.total_return()) * 100, 2), "%")
print("Trades       :", int(pf.trades.count()))
print("Max drawdown :", round(float(pf.max_drawdown()) * 100, 2), "%")
print("\nThe regime filter is what stops momentum from buying into a crash.")
```

Live output

```
Momentum + 200-SMA regime filter on ICICIBANK
Total return : -9.76 %
Trades       : 8
Max drawdown : -11.29 %

The regime filter is what stops momentum from buying into a crash.
```

Heads up
A negative or middling backtest on a short window is normal and honest - single-stock momentum is noisy, and one name over one year tells you little. The real strategy diversifies across the whole ranked basket and rebalances regularly, which smooths the ride dramatically. Never judge a momentum system on one stock; judge it on the portfolio.
## Try it yourself
  * Change the momentum lookback in `02_cross_sectional_momentum.py` from 60 days to 120 and see how the ranking shifts.
  * In the ATR breakout, raise the multiplier from 1.0 to 2.0 - fewer but more decisive breakouts. Count how many remain.
  * Swap the regime filter's 200-day SMA for a 100-day one in `06_regime_filter.py`. A faster filter reacts sooner but whipsaws more - which do you prefer?


## Recap
  * **Cross-sectional momentum** ranks a basket of stocks by recent return and holds the leaders.
  * **ATR** measures daily movement in rupees; an **ATR breakout** demands a volatility-sized move, sidestepping noise.
  * The **Bollinger squeeze** (low bandwidth) flags quiet coils that often precede big expansions.
  * A **regime filter** (price above the 200-day SMA) keeps momentum from buying into a downtrend.
  * **Volatility targeting** sizes positions as `target_vol / realised_vol`, keeping risk constant across calm and wild markets - always with a leverage cap.
  * These tools are **market-agnostic** : the same ATR breakout works on NSE equities and MCX commodities alike.


Next we look at the calendar itself - day-of-week, month and expiry-week effects you can measure straight from history.
On this page
