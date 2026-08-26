Chapters
Module D · Signals & Scanning - Chapter 17
# From Indicators to Trading Signals
Build precise, de-duplicated entry and exit signals you can trust in a backtest.
NSE
What you'll learn
  * ·Boolean conditions
  * ·crossover / crossunder
  * ·exrem to remove repeats
  * ·flip for stateful holds
  * ·valuewhen lookups
  * ·Shifting to avoid look-ahead


An indicator on its own never tells you what to _do_. A 20-day EMA is just a wavy line; RSI is just a number bouncing between 0 and 100. The moment you turn one of those into a rule - _"buy when the fast average crosses above the slow one, sell when it crosses back"_ - you've created a **signal**. This chapter is about doing that cleanly, because the gap between a sloppy signal and a clean one is the gap between a backtest you can trust and one that quietly lies to you.
We'll work almost entirely with the helper functions from `openalgo.ta` that you met at the end of Chapter 16 - `crossover`, `crossunder`, `exrem`, `flip`, `valuewhen` - plus one habit that matters more than all of them: never act on information you couldn't have had yet. By the end you'll be able to take any indicator and produce two tidy arrays of `True`/`False` - _entries_ and _exits_ - that a backtester can consume directly.

```
from openalgo import api, ta

```

That single import line gives you both the market connection (`api`) and the indicator toolkit (`ta`). Every example in this chapter uses it.
## A signal is a yes/no question asked of every bar
Here's the mental shift. In Chapter 2 you asked one question about one number with `if`. A signal asks the _same_ question about _every bar in your history at once_ , and hands back a column of `True`/`False` answers. That column is called a **boolean Series** - "boolean" just means it holds only `True` or `False`.
The simplest signal of all: _is the close above its 20-day EMA?_ You write it almost exactly as you'd say it.
EX 1A signal is a boolean questionNSEch17/01_boolean_conditions.py
Copy
```
# A trade signal is just a True/False question asked of every bar at once.
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

close = df["close"]
ema20 = ta.ema(close, 20)

# "Is price above its 20-day EMA?" -- one boolean answer per bar.
above = close > ema20

print("Bars where price is above EMA20:", int(above.sum()), "of", len(above))
print("Most recent answer:", bool(above.iloc[-1]))
print(above.tail(5))
```

Live output

```
Bars where price is above EMA20: 24 of 80
Most recent answer: False
timestamp
2026-06-17     True
2026-06-18     True
2026-06-19    False
2026-06-22     True
2026-06-23    False
dtype: bool
```

Notice `close > ema20` produces not one answer but one per day, aligned to the same dates. That alignment is the whole point - pandas keeps every value matched to its timestamp, so you never accidentally compare Monday's price to Tuesday's average.
## Combining conditions with and / or
One condition is rarely enough. Real rules stack them: _trade only when price is above its trend line**and** momentum agrees._ In pandas you combine boolean Series with `&` (and) and `|` (or) - not the words `and`/`or`, which don't work element by element.
EX 2Stack conditions with & andch17/02_combine_conditions.py
Copy
```
# Real signals combine several questions with & (and) and | (or).
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

close = df["close"]
ema50 = ta.ema(close, 50)
rsi = ta.rsi(close, 14)

# A "trend-with-momentum" filter: price above EMA50 AND RSI above 50.
# Each side is wrapped in ( ) -- a habit that avoids hard-to-find bugs.
bullish = (close > ema50) & (rsi > 50)

print("Days passing BOTH conditions:", int(bullish.sum()))
print("Today -- above EMA50:", bool((close > ema50).iloc[-1]),
      "| RSI>50:", bool((rsi > 50).iloc[-1]),
      "| signal:", bool(bullish.iloc[-1]))
```

Live output

```
Days passing BOTH conditions: 9
Today -- above EMA50: False | RSI>50: False | signal: False
```

Heads up
Always wrap each condition in parentheses: `(close > ema50) & (rsi > 50)`. Without them, Python's operator precedence reads the line in the wrong order and you get a confusing error or - worse - a silently wrong result. Parentheses around every condition is a habit that pays for itself.
## Crossovers: catching the exact moment of change
"Price is above the EMA" is true for long stretches. But you don't want to buy on _every_ one of those days - you want to buy on the _one day it first becomes true_. That precise turning point is a **crossover** , and `ta.crossover(fast, slow)` marks exactly the bar where the first series crosses above the second.
EX 3Mark the crossover barNSEch17/03_crossover.py
Copy
```
# ta.crossover marks the single bar where a fast line crosses ABOVE a slow line.
import os
from datetime import datetime, timedelta

import pandas as pd
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=250)).strftime("%Y-%m-%d")
df = client.history(symbol="INFY", exchange="NSE", interval="D", start_date=start, end_date=end)

close = df["close"]
ema_fast = ta.ema(close, 10)
ema_slow = ta.ema(close, 20)

# crossover/crossunder return a NumPy array, not a Series.
# Wrap it back into a Series so it lines up with the DataFrame's dates.
cross_up = pd.Series(ta.crossover(ema_fast, ema_slow), index=df.index)

print("Type returned by ta.crossover:", type(ta.crossover(ema_fast, ema_slow)).__name__)
print("Bullish crosses in the window:", int(cross_up.sum()))
print("Dates of those crosses:")
print(close[cross_up].tail())
```

Live output

```
Type returned by ta.crossover: ndarray
Bullish crosses in the window: 4
Dates of those crosses:
timestamp
2025-10-23    1496.1
2026-01-16    1654.0
2026-04-08    1317.7
2026-06-02    1243.9
Name: close, dtype: float64
```

Key idea
`ta.crossover` and `ta.crossunder` return a **NumPy array** , not a pandas Series. An array has no dates attached. To line it back up with your DataFrame - so you can filter rows or `.shift()` it later - wrap it: `pd.Series(arr, index=df.index)`. You'll do this constantly, so it's worth committing to memory.
Its mirror image, `ta.crossunder(fast, slow)`, marks where the fast line drops _below_ the slow one - a natural exit for a long trade. Together they give you raw entries and exits.
EX 4Entries and exits from a crossNSEch17/04_crossunder_exit.py
Copy
```
# ta.crossunder is the mirror image -- the bar where fast crosses BELOW slow.
# Pair it with crossover and you have raw entries and exits.
import os
from datetime import datetime, timedelta

import pandas as pd
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=250)).strftime("%Y-%m-%d")
df = client.history(symbol="HDFCBANK", exchange="NSE", interval="D", start_date=start, end_date=end)

close = df["close"]
fast, slow = ta.ema(close, 10), ta.ema(close, 20)

buy = pd.Series(ta.crossover(fast, slow), index=df.index)
sell = pd.Series(ta.crossunder(fast, slow), index=df.index)

print("Raw BUY signals :", int(buy.sum()))
print("Raw SELL signals:", int(sell.sum()))
print("Last 3 buy dates :", list(close[buy].tail(3).index.strftime("%Y-%m-%d")))
print("Last 3 sell dates:", list(close[sell].tail(3).index.strftime("%Y-%m-%d")))
```

Live output

```
Raw BUY signals : 3
Raw SELL signals: 2
Last 3 buy dates : ['2025-10-17', '2025-11-20', '2026-06-16']
Last 3 sell dates: ['2025-11-03', '2025-12-16']
```

## Removing repeated signals with exrem
Run the raw signals on enough data and you'll spot a problem: sometimes two buy signals fire before any sell, or the indicator chops around and triggers a flurry. If you blindly acted on each, you'd "buy" a stock you already own. **`ta.exrem`**("excess removal") fixes this by keeping a signal only until the opposite one arrives - forcing buys and sells to strictly alternate.
EX 5Remove repeated signalsNSEch17/05_exrem_dedupe.py
Copy
```
# ta.exrem removes repeated signals so you don't buy twice before selling once.
import os
from datetime import datetime, timedelta

import pandas as pd
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=300)).strftime("%Y-%m-%d")
df = client.history(symbol="ICICIBANK", exchange="NSE", interval="D", start_date=start, end_date=end)

close = df["close"]
rsi = ta.rsi(close, 14)

# Raw level rules fire on EVERY qualifying bar, so an oversold or overbought
# stretch triggers a whole flurry of repeated buys (or sells).
raw_buy = pd.Series((rsi < 30).to_numpy(), index=df.index)    # buy while oversold
raw_sell = pd.Series((rsi > 55).to_numpy(), index=df.index)   # sell once recovered

# exrem(primary, secondary): keep a primary signal only until the next secondary.
clean_buy = pd.Series(ta.exrem(raw_buy, raw_sell), index=df.index)
clean_sell = pd.Series(ta.exrem(raw_sell, raw_buy), index=df.index)

print(f"{'':12s}{'raw':>6s}{'cleaned':>10s}")
print(f"{'BUY':12s}{int(raw_buy.sum()):>6d}{int(clean_buy.sum()):>10d}")
print(f"{'SELL':12s}{int(raw_sell.sum()):>6d}{int(clean_sell.sum()):>10d}")
print("exrem collapsed each flurry to its FIRST signal -- buys and sells now alternate.")
```

Live output

```
raw   cleaned
BUY              7         2
SELL            47         3
exrem collapsed each flurry to its FIRST signal -- buys and sells now alternate.
```

Read `ta.exrem(buy, sell)` as: _"keep each buy, but ignore any further buys until a sell has happened."_ The result is a clean, alternating sequence - exactly what an order system expects.
## Holding a position with flip
Entries and exits tell you _when_ something happens. Often you also want to know _where you stand right now_ - am I in a trade or flat? **`ta.flip(on, off)`**answers that. It switches to`1` (in position) on every entry bar and stays there until an exit bar flips it back to `0`. It's a stateful "in-position" flag that fills the gaps between your signals.
EX 6A stateful in-position flagNSEch17/06_flip_hold.py
Copy
```
# ta.flip turns one-bar entry/exit signals into a held position (an "in trade" flag).
import os
from datetime import datetime, timedelta

import pandas as pd
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=200)).strftime("%Y-%m-%d")
df = client.history(symbol="SBIN", exchange="NSE", interval="D", start_date=start, end_date=end)

close = df["close"]
fast, slow = ta.ema(close, 10), ta.ema(close, 20)
buy = pd.Series(ta.crossover(fast, slow), index=df.index)
sell = pd.Series(ta.crossunder(fast, slow), index=df.index)

# flip(on, off) = 1 from a buy bar onward, back to 0 from the next sell bar.
in_position = pd.Series(ta.flip(buy, sell), index=df.index).astype(int)

print("Bars spent in a position:", int(in_position.sum()), "of", len(in_position))
print("Currently in a trade:", "YES" if in_position.iloc[-1] else "NO")
print(in_position.tail(8))
```

Live output

```
Bars spent in a position: 75 of 134
Currently in a trade: YES
timestamp
2026-06-12    1
2026-06-15    1
2026-06-16    1
2026-06-17    1
2026-06-18    1
2026-06-19    1
2026-06-22    1
2026-06-23    1
dtype: int64
```

That flag is the bridge to a backtest: multiply it by daily returns and you have the return of _being in the trade_ - a trick we lean on in Chapter 19 and formalise with VectorBT in Chapter 26.
## Looking up the entry price with valuewhen
Once you're in a trade you'll want to know your entry price - to measure open profit, set a stop, or size the next order. **`ta.valuewhen(condition, values, n)`**returns the value from`values` the last time `condition` was true. With `n=1` it's the most recent occurrence; `n=2` is the one before that.
EX 7Grab the price at the last signalNSEch17/07_valuewhen.py
Copy
```
# ta.valuewhen grabs the price (or any value) at the most recent signal bar.
import os
from datetime import datetime, timedelta

import pandas as pd
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=250)).strftime("%Y-%m-%d")
df = client.history(symbol="RELIANCE", exchange="NSE", interval="D", start_date=start, end_date=end)

close = df["close"]
fast, slow = ta.ema(close, 10), ta.ema(close, 20)
buy = pd.Series(ta.crossover(fast, slow), index=df.index)

# At every bar, what was the close on the LAST buy signal? (n=1 = most recent)
entry_price = pd.Series(ta.valuewhen(buy, close, 1), index=df.index)
open_pnl_pct = (close - entry_price) / entry_price * 100

print("Last entry price the signal would have used:", round(float(entry_price.iloc[-1]), 2))
print("Latest close:", round(float(close.iloc[-1]), 2))
print("Open P&L since that entry: {:.2f}%".format(float(open_pnl_pct.iloc[-1])))
```

Live output

```
Last entry price the signal would have used: 1425.4
Latest close: 1306.0
Open P&L since that entry: -8.38%
```

Here we ask: _at every bar, what was the close on the most recent buy signal?_ Subtract it from today's close and you have live, running open profit - without writing a single loop.
## The look-ahead trap
This is the most important idea in the chapter, so slow down. A crossover is confirmed using a bar's **closing** price. But you only _know_ the close once the bar is over - by then you can't trade at that price any more. If your backtest buys at the same close that produced the signal, it's quietly assuming you can see the future. That's **look-ahead bias** , and it's the single most common reason a strategy looks brilliant on paper and falls apart live.
The fix is one method: `.shift(1)`. It pushes every signal forward by one bar, so a cross seen on Monday's close becomes a trade on Tuesday.
EX 8Shift to avoid look-aheadMCXch17/08_lookahead_shift.py
Copy
```
# The look-ahead trap: a signal on today's CLOSE can only be acted on TOMORROW.
# .shift(1) moves the signal forward one bar so the backtest stays honest.
import os
from datetime import datetime, timedelta

import pandas as pd
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=200)).strftime("%Y-%m-%d")
df = client.history(symbol="GOLDM03JUL26FUT", exchange="MCX", interval="D", start_date=start, end_date=end)

close = df["close"]
fast, slow = ta.ema(close, 10), ta.ema(close, 20)
signal_today = pd.Series(ta.crossover(fast, slow), index=df.index)

# Shift the signal: a cross seen on close[t] becomes tradable on bar t+1.
tradable = signal_today.shift(1).fillna(False)

cmp = pd.DataFrame({"close": close, "signal_today": signal_today, "tradable_next_bar": tradable})
print(cmp.tail(6))
print("Acting on 'tradable_next_bar' avoids buying at a price you couldn't have known yet.")
```

Live output

```
close  signal_today  tradable_next_bar
timestamp                                          
2026-06-16  150985         False              False
2026-06-17  151747         False              False
2026-06-18  147424         False              False
2026-06-19  145221         False              False
2026-06-22  146125         False              False
2026-06-23  144287         False              False
Acting on 'tradable_next_bar' avoids buying at a price you couldn't have known yet.
```

Tip
The rule of thumb: **act on the previous bar's signal.** Anything you compute from a bar's close - crossovers, RSI levels, breakouts - can only be traded from the _next_ bar onward. A single `.shift(1)` turns an optimistic, untradeable backtest into an honest one.
## Putting it all together
Now we chain the whole pipeline: compute two EMAs, find the raw crosses, de-duplicate them with `exrem`, and shift them so they're tradable. The output is two boolean arrays - `entries` and `exits` - ready to hand straight to a backtester.
EX 9A clean signal pipeline end to endNSEch17/09_full_signal_pipeline.py
Copy
```
# End to end: build clean, shifted entry+exit arrays for an EMA crossover.
import os
from datetime import datetime, timedelta

import pandas as pd
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=300)).strftime("%Y-%m-%d")
df = client.history(symbol="RELIANCE", exchange="NSE", interval="D", start_date=start, end_date=end)

close = df["close"]
fast, slow = ta.ema(close, 20), ta.ema(close, 50)

raw_buy = pd.Series(ta.crossover(fast, slow), index=df.index)
raw_sell = pd.Series(ta.crossunder(fast, slow), index=df.index)

# 1) de-duplicate so entries/exits alternate, 2) shift to trade on the next bar.
entries = pd.Series(ta.exrem(raw_buy, raw_sell), index=df.index).shift(1).fillna(False)
exits = pd.Series(ta.exrem(raw_sell, raw_buy), index=df.index).shift(1).fillna(False)

print("Final tradable entries:", int(entries.sum()), "| exits:", int(exits.sum()))
print("These two boolean arrays are exactly what a backtester (Chapter 26) consumes.")
print(pd.DataFrame({"close": close, "entry": entries, "exit": exits})[entries | exits].tail())
```

Live output

```
Final tradable entries: 3 | exits: 4
These two boolean arrays are exactly what a backtester (Chapter 26) consumes.
             close  entry   exit
timestamp                       
2025-10-01  1368.7  False   True
2025-10-20  1466.8   True  False
2026-01-19  1413.6  False   True
2026-05-08  1435.2   True  False
2026-05-14  1361.8  False   True
```

That's the template you'll reuse for the rest of the series. Indicator in, two clean boolean arrays out. Swap the EMAs for a Supertrend or an RSI rule and the _shape_ of the code never changes.
## Try it yourself
  * In the combine-conditions example, add a third filter - say `rsi < 70` - so you avoid buying into an already-overbought move.
  * Take the full pipeline and change the EMAs from 20/50 to 10/30. Do you get more signals or fewer? Does that feel like more noise or more edge?
  * Remove the `.shift(1)` from the pipeline and compare the entry dates. Convince yourself why trading on the same bar would be cheating.


## Recap
  * A **signal** is a boolean Series - a `True`/`False` answer for every bar, kept aligned to its dates.
  * Combine conditions with `&` and `|`, and **always wrap each in parentheses**.
  * `ta.crossover` / `ta.crossunder` mark the exact turning bar and return **NumPy arrays** - wrap them with `pd.Series(arr, index=df.index)`.
  * `ta.exrem` removes repeated signals so entries and exits alternate; `ta.flip` gives a stateful in-position flag.
  * `ta.valuewhen` looks up the value (like the entry price) at the last time a condition was true.
  * **`.shift(1)`defeats look-ahead bias** - always act on the previous bar's signal.


Clean signals are only half the job. Next we point them at _the whole market at once_ - looping a signal across dozens of symbols to build a scanner that surfaces the handful worth your attention.
On this page
