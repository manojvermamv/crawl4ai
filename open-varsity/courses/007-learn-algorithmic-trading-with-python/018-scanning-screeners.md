Chapters
Module D · Signals & Scanning - Chapter 18
# Scanning & Screeners
Run a signal across dozens of symbols and rank the results.
NSENFOMCX
What you'll learn
  * ·Loop a universe
  * ·RSI / EMA screens
  * ·Breakout scan
  * ·Relative-volume scan
  * ·Rank & sort hits
  * ·Scan across exchanges


You now know how to turn an indicator into a clean signal for _one_ stock. But a single chart is a keyhole view of the market. The real power of code - the thing no human can match - is asking the _same_ question of fifty stocks before your coffee cools. That's a **scanner** : a loop that runs a rule across a list of symbols and hands back only the names that pass.
This chapter builds scanners from the ground up. We'll screen for oversold RSI, for price above a trend line, for fresh breakouts, and for unusual volume - then rank the hits into a tidy table you could act on. The logic is deliberately simple, because the value of a scanner isn't clever maths; it's _coverage_. A plain RSI rule across a hundred names will find you more opportunities than the world's best indicator on one.

```
from openalgo import api, ta

```

## The shape of every scanner
Strip a scanner to its bones and it's just three things: a **universe** (the list of symbols to check), a **loop** over that universe, and a **rule** applied to each. Everything else is decoration.
EX 1The simplest possible scannerNSEch18/01_universe_loop.py
Copy
```
# A scanner is just a loop over a universe. Start with the simplest version.
import os
from datetime import datetime, timedelta

import pandas as pd
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

universe = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "SBIN"]

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")


def daily(sym, exchange="NSE"):
    # Return a clean OHLCV frame, or None if the server hiccups on one symbol.
    df = client.history(symbol=sym, exchange=exchange, interval="D", start_date=start, end_date=end)
    return df if isinstance(df, pd.DataFrame) and not df.empty else None


print(f"{'SYMBOL':12s}{'CLOSE':>10s}{'RSI14':>8s}")
for sym in universe:
    df = daily(sym)
    if df is None:
        print(f"{sym:12s}{'no data':>10s}")
        continue
    rsi = ta.rsi(df["close"], 14)
    print(f"{sym:12s}{df['close'].iloc[-1]:>10.2f}{rsi.iloc[-1]:>8.1f}")
```

Live output

```
SYMBOL           CLOSE   RSI14
RELIANCE       1306.00    45.3
TCS            2060.00    32.4
INFY           1029.00    32.5
HDFCBANK        772.90    51.4
ICICIBANK      1335.50    61.0
SBIN           1023.60    55.6
```

Look at the little `daily()` helper. It fetches history and returns `None` if the response isn't a proper DataFrame. That guard matters: on a shared data server, _one_ symbol out of twelve might occasionally hand back an error instead of candles, and without the guard your whole scan would crash on that single name.
Heads up
A scanner that dies on the first bad symbol is useless - it'll fail at the worst possible moment, mid-scan, leaving you blind. Always make the loop survive one bad response and move on. The `if df is None: continue` pattern below is the cheapest insurance you'll ever buy.
## Screening on RSI
The first real screen: only show me names that are stretched. We loop our universe, compute RSI for each, and collect the ones below 30 (oversold - possibly due a bounce) or above 70 (overbought - possibly due a pullback).
EX 2Screen for oversold and overboughtNSEch18/02_rsi_screen.py
Copy
```
# RSI screen: list only the names that are oversold or overbought right now.
import os
from datetime import datetime, timedelta

import pandas as pd
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

universe = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "SBIN",
            "AXISBANK", "WIPRO", "ITC", "LT", "MARUTI", "KOTAKBANK"]

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")


def daily(sym):
    df = client.history(symbol=sym, exchange="NSE", interval="D", start_date=start, end_date=end)
    return df if isinstance(df, pd.DataFrame) and not df.empty else None


oversold, overbought = [], []
for sym in universe:
    df = daily(sym)
    if df is None:
        continue
    r = float(ta.rsi(df["close"], 14).iloc[-1])
    if r < 30:
        oversold.append((sym, round(r, 1)))
    elif r > 70:
        overbought.append((sym, round(r, 1)))

print("Oversold (RSI < 30) :", oversold or "none")
print("Overbought (RSI > 70):", overbought or "none")
print(f"Scanned {len(universe)} names.")
```

Live output

```
Oversold (RSI < 30) : none
Overbought (RSI > 70): none
Scanned 12 names.
```

This is the heart of a mean-reversion watchlist. Run it each morning and instead of eyeballing a dozen charts, you read a two-line answer.
## Screening on trend: price above its EMA
Momentum and trend traders want the opposite of oversold - they want strength. A simple, robust filter: _is the stock trading above its 50-day EMA?_ We collect every name that is, and sort them by how far above they sit, so the strongest float to the top.
EX 3Rank names above their EMA50NSEch18/03_above_ema_screen.py
Copy
```
# Trend screen: which names are trading above their 50-day EMA?
import os
from datetime import datetime, timedelta

import pandas as pd
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

universe = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "SBIN",
            "AXISBANK", "WIPRO", "ITC", "LT", "MARUTI", "KOTAKBANK"]

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=150)).strftime("%Y-%m-%d")


def daily(sym):
    df = client.history(symbol=sym, exchange="NSE", interval="D", start_date=start, end_date=end)
    return df if isinstance(df, pd.DataFrame) and not df.empty else None


in_uptrend = []
for sym in universe:
    df = daily(sym)
    if df is None:
        continue
    close = df["close"].iloc[-1]
    ema50 = float(ta.ema(df["close"], 50).iloc[-1])
    if close > ema50:
        in_uptrend.append((sym, round((close / ema50 - 1) * 100, 1)))

in_uptrend.sort(key=lambda x: x[1], reverse=True)
print(f"{len(in_uptrend)}/{len(universe)} names are above their EMA50.")
print("Symbol  % above EMA50")
for sym, pct in in_uptrend:
    print(f"{sym:10s}{pct:>6.1f}%")
```

Live output

```
6/12 names are above their EMA50.
Symbol  % above EMA50
LT           4.1%
AXISBANK     4.0%
KOTAKBANK    3.4%
ICICIBANK    3.0%
MARUTI       0.6%
SBIN         0.4%
```

## Scanning for breakouts
A **breakout** is a close pushing above a level it couldn't clear before - often the highest high of the last N days. `ta.highest(series, N)` gives the rolling N-bar high; comparing today's close to _yesterday's_ N-day high tells you a fresh breakout just happened.
EX 4Find new 20-day-high breakoutsNSEch18/04_breakout_scan.py
Copy
```
# Breakout scan: close making a new 20-day high. ta.highest does the heavy lifting.
import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

universe = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "SBIN",
            "AXISBANK", "WIPRO", "ITC", "LT", "MARUTI", "KOTAKBANK"]

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
N = 20


def daily(sym):
    df = client.history(symbol=sym, exchange="NSE", interval="D", start_date=start, end_date=end)
    return df if isinstance(df, pd.DataFrame) and not df.empty else None


breakouts = []
for sym in universe:
    df = daily(sym)
    if df is None:
        continue
    # highest high over the PRIOR N bars -- index [-2] excludes today's own bar.
    prior_high = np.asarray(ta.highest(df["high"], N))[-2]
    last_close = float(df["close"].iloc[-1])
    if last_close > prior_high:
        breakouts.append((sym, last_close, round(float(prior_high), 2)))

print(f"New {N}-day-high breakouts:")
for sym, c, h in breakouts:
    print(f"  {sym:10s} close {c:>9.2f}  cleared prior high {h:>9.2f}")
print("Total:", len(breakouts))
```

Live output

```
New 20-day-high breakouts:
Total: 0
```

Key idea
Notice we take the highest high at index `[-2]`, not `[-1]`. The value at `[-1]` already includes today's bar, so today's close can never beat a high it helped set - the test would always fail. Using `[-2]` compares today against the channel _as it stood yesterday_. The same one-bar care from the look-ahead lesson in Chapter 17 applies to scans too.
## Scanning for unusual volume
Price tells you _what_ ; volume tells you _how serious_. **Relative volume** (or "RVOL") divides today's volume by its recent average - a reading of 2.0 means twice the usual interest, which often precedes or confirms a real move. We compute it across the universe and sort the busiest names first.
EX 5Rank by relative volumeNSEch18/05_relative_volume_scan.py
Copy
```
# Relative-volume scan: today's volume vs its 20-day average. >1.5 means unusual interest.
import os
from datetime import datetime, timedelta

import pandas as pd
from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

universe = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "SBIN",
            "AXISBANK", "WIPRO", "ITC", "LT", "MARUTI", "KOTAKBANK"]

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")


def daily(sym):
    df = client.history(symbol=sym, exchange="NSE", interval="D", start_date=start, end_date=end)
    return df if isinstance(df, pd.DataFrame) and not df.empty else None


rows = []
for sym in universe:
    df = daily(sym)
    if df is None:
        continue
    avg20 = df["volume"].rolling(20).mean().iloc[-1]
    rvol = df["volume"].iloc[-1] / avg20 if avg20 else 0
    rows.append((sym, round(float(rvol), 2)))

rows.sort(key=lambda x: x[1], reverse=True)
print("Relative volume (today / 20-day avg), highest first:")
for sym, rvol in rows:
    flag = "  <-- elevated" if rvol > 1.5 else ""
    print(f"  {sym:10s}{rvol:>6.2f}x{flag}")
```

Live output

```
Relative volume (today / 20-day avg), highest first:
  INFY        1.13x
  LT          1.08x
  TCS         1.03x
  MARUTI      0.93x
  RELIANCE    0.83x
  AXISBANK    0.77x
  SBIN        0.72x
  WIPRO       0.72x
  ICICIBANK   0.71x
  HDFCBANK    0.69x
  KOTAKBANK   0.68x
  ITC         0.53x
```

## Ranking the hits into a table
Individual screens are useful, but the professional move is to gather several metrics per symbol into a single table and _rank_ it. Pandas makes this clean: build a list of dictionaries, turn it into a DataFrame, and call `.sort_values()`. Here we rank the universe by 20-day return, the simplest momentum score.
EX 6Build and rank a results tableNSEch18/06_rank_table.py
Copy
```
# Gather several metrics per name into a pandas table, then rank by momentum.
import os
from datetime import datetime, timedelta

import pandas as pd
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

universe = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "SBIN",
            "AXISBANK", "WIPRO", "ITC", "LT", "MARUTI", "KOTAKBANK"]

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")


def daily(sym):
    df = client.history(symbol=sym, exchange="NSE", interval="D", start_date=start, end_date=end)
    return df if isinstance(df, pd.DataFrame) and not df.empty else None


rows = []
for sym in universe:
    df = daily(sym)
    if df is None:
        continue
    close = df["close"]
    ret_20 = (close.iloc[-1] / close.iloc[-21] - 1) * 100  # 20-day return
    rows.append({"symbol": sym,
                 "close": round(float(close.iloc[-1]), 2),
                 "rsi14": round(float(ta.rsi(close, 14).iloc[-1]), 1),
                 "ret_20d_%": round(float(ret_20), 2)})

table = pd.DataFrame(rows).sort_values("ret_20d_%", ascending=False).reset_index(drop=True)
table.index += 1  # rank starts at 1
print("Universe ranked by 20-day return (strongest first):")
print(table.to_string())
```

Live output

```
Universe ranked by 20-day return (strongest first):
       symbol     close  rsi14  ret_20d_%
1        SBIN   1023.60   55.3       5.57
2    AXISBANK   1358.00   63.9       3.57
3          LT   4169.80   60.7       3.38
4   ICICIBANK   1335.50   60.5       3.38
5   KOTAKBANK    401.90   60.9       2.30
6      MARUTI  13430.00   53.8       1.97
7    HDFCBANK    772.90   50.9      -1.77
8         ITC    290.00   50.6      -1.99
9    RELIANCE   1306.00   45.6      -4.46
10       INFY   1029.00   32.3     -10.04
11        TCS   2060.00   31.7     -10.75
12      WIPRO    174.39   30.6     -15.69
```

A ranked table is the natural output of any scanner - it turns "here are twelve stocks" into "here are the three that matter most, in order." That ranking idea becomes a full strategy in the next chapter.
## The same pattern, any exchange
Nothing about a scanner is tied to equities. Swap the symbol list and the exchange and the loop is identical - here a handful of MCX commodity futures, screened for RSI and trend just like the stocks were.
EX 7Scan an MCX commodity listMCXch18/07_mcx_scan.py
Copy
```
# The same scanner pattern works on any exchange -- here a small MCX commodity list.
import os
from datetime import datetime, timedelta

import pandas as pd
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# MCX futures carry their own symbol + expiry; the loop logic is unchanged.
mcx = ["GOLDM03JUL26FUT", "SILVERM30JUN26FUT", "CRUDEOIL20JUL26FUT"]

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")

print(f"{'SYMBOL':20s}{'CLOSE':>12s}{'RSI14':>8s}{'TREND':>10s}")
for sym in mcx:
    df = client.history(symbol=sym, exchange="MCX", interval="D", start_date=start, end_date=end)
    if not (isinstance(df, pd.DataFrame) and not df.empty):
        print(f"{sym:20s}{'no data':>12s}")
        continue
    close = df["close"].iloc[-1]
    rsi = float(ta.rsi(df["close"], 14).iloc[-1])
    trend = "up" if close > float(ta.ema(df["close"], 20).iloc[-1]) else "down"
    print(f"{sym:20s}{close:>12.2f}{rsi:>8.1f}{trend:>10s}")
```

Live output

```
SYMBOL                     CLOSE   RSI14     TREND
GOLDM03JUL26FUT        144300.00    32.5      down
SILVERM30JUN26FUT      231038.00    32.8      down
CRUDEOIL20JUL26FUT       6951.00    33.2      down
```

## A faster live snapshot with multiquotes
When you only need _current_ numbers - last price and the day's change, not full history - looping `history()` is wasteful. One `multiquotes()` call fetches a whole basket in a single round trip, across exchanges. Here we mix NSE stocks with an NFO index future and rank them by the day's move.
EX 8A fast multi-exchange snapshotNSENFOch18/08_multiquotes_scan.py
Copy
```
# For a live snapshot scan, one multiquotes() call beats a loop of single quotes.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# Mix exchanges freely -- NSE equity plus an NFO future in one request.
watch = [
    {"symbol": "RELIANCE", "exchange": "NSE"},
    {"symbol": "TCS", "exchange": "NSE"},
    {"symbol": "INFY", "exchange": "NSE"},
    {"symbol": "NIFTY30JUN26FUT", "exchange": "NFO"},
]

resp = client.multiquotes(symbols=watch)
movers = []
for r in resp["results"]:
    d = r["data"]
    chg = (d["ltp"] - d["prev_close"]) / d["prev_close"] * 100 if d["prev_close"] else 0
    movers.append((r["symbol"], r["exchange"], d["ltp"], round(chg, 2)))

movers.sort(key=lambda x: x[3], reverse=True)
print(f"{'SYMBOL':20s}{'EXCH':6s}{'LTP':>12s}{'CHG%':>9s}")
for sym, ex, ltp, chg in movers:
    print(f"{sym:20s}{ex:6s}{ltp:>12.2f}{chg:>8.2f}%")
```

Live output

```
SYMBOL              EXCH           LTP     CHG%
RELIANCE            NSE        1309.50   -1.28%
NIFTY30JUN26FUT     NFO       23810.00   -1.30%
TCS                 NSE        2059.60   -3.21%
INFY                NSE        1029.30   -3.39%
```

Tip
Rule of thumb: use `multiquotes()` when you need a live snapshot of many symbols _right now_ , and loop `history()` when each name needs its own indicator computed over time. One round trip beats fifty whenever the data you need is just the latest quote.
## Try it yourself
  * Add five stocks you actually follow to the universe and re-run the RSI screen. Did anything interesting show up?
  * Change the breakout window from 20 days to 50. Fewer, higher-quality breakouts - or none at all this week?
  * In the ranking table, sort by `rsi14` instead of `ret_20d_%`. Does the leaderboard change character?


## Recap
  * A scanner is just a **universe + a loop + a rule** - coverage beats cleverness.
  * Guard every loop so one bad symbol response can't crash the whole scan (`if df is None: continue`).
  * `ta.highest` (or a rolling max) powers breakout scans - compare today's close to _yesterday's_ N-day high.
  * **Relative volume** flags unusual participation; ranking by it surfaces the busy names.
  * Collect metrics into a pandas DataFrame and `.sort_values()` to turn a list into a leaderboard.
  * The identical loop works on MCX and NFO; `multiquotes()` is the efficient choice for live snapshots of many symbols.


We've been ranking stocks all chapter. Next we promote that ranking from a watchlist into an actual **strategy** - delivery-style equity systems that decide what to hold, from golden crosses to momentum rotation.
On this page
