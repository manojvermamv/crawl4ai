Chapters
Module A · Foundations - Chapter 05
# Historical Data & Timeframes
Fetch OHLCV history at any interval and reshape it for analysis.
NSENFOMCX
What you'll learn
  * ·history() OHLCV
  * ·Intervals from 1m to D
  * ·Date ranges
  * ·Multi-symbol download
  * ·api vs db source
  * ·Resampling timeframes


A live quote tells you where a stock is _right now_. But you can't backtest a hunch on a single price, you can't spot a trend in one number, and you can't measure how wild or calm a stock has been from a snapshot. For all of that you need the _past_ - the stock's history, candle by candle.
This chapter is about pulling that history down onto your machine. One function does almost all the work: `client.history()`. By the end you'll be able to download any instrument's price history at any timeframe - from one-minute candles to daily - across stocks, futures and commodities, reshape it into bigger candles, and save it to a file for later. This is the raw material of every chart, every indicator, and every backtest in the rest of this series.
## What is OHLCV history?
When you ask for history, you don't get back one number per day - you get a **candle** for each period. A candle packs five facts about that slice of time, abbreviated **OHLCV** :
  * **Open** - the price at the start of the period.
  * **High** - the highest price reached.
  * **Low** - the lowest price reached.
  * **Close** - the price at the end. This is the number traders quote most often.
  * **Volume** - how many shares or contracts changed hands.


`client.history()` hands all of this back as a **DataFrame** - a spreadsheet-like table from the pandas library (we'll properly master pandas in Chapter 7). Each row is one candle, the rows are indexed by their **timestamp** , and the columns are `close high low oi open volume` (the `oi`, _open interest_ , is only meaningful for derivatives - it's zero for stocks).
Let's pull four months of daily candles for Reliance and look at the shape of what comes back.
EX 1Download daily OHLCV candlesNSEch05/01_daily_history.py
Copy
```
# The workhorse call: download daily OHLCV candles into a DataFrame.
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")

df = client.history(symbol="RELIANCE", exchange="NSE", interval="D", start_date=start, end_date=end)
print("Shape  :", df.shape)
print("Columns:", df.columns.tolist())
print(df.tail(3))
```

Live output

```
Shape  : (80, 6)
Columns: ['close', 'high', 'low', 'oi', 'open', 'volume']
             close    high     low  oi    open    volume
timestamp                                               
2026-06-19  1309.5  1338.2  1305.3   0  1328.0  24887034
2026-06-22  1326.5  1344.9  1314.1   0  1316.7  12931213
2026-06-23  1306.0  1333.0  1304.0   0  1328.9  15277531
```

The `.shape` tells you `(rows, columns)` - so `(80, 6)` means 80 daily candles, each with 6 values. `.tail(3)` prints the last three rows. Notice the call's five ingredients, the same every time: a **symbol** , an **exchange** , an **interval** , and a **start** and **end** date.
Note
We build the dates with Python's `datetime` and `timedelta`: `datetime.now()` is today, and subtracting a `timedelta(days=120)` walks back four months. Doing it this way keeps the example **evergreen** - it always asks for "the last 120 days" relative to whenever you run it, instead of a hard-coded date that goes stale.
## Intervals: from one minute to one day
The **interval** is the size of each candle. Ask for `"D"` and each row is one trading day; ask for `"5m"` and each row is five minutes of trading. OpenAlgo supports `1m 3m 5m 10m 15m 30m 60m 1h D`. Smaller intervals show you fine detail intraday; bigger ones show you the longer-term shape.
Here's the exact same call as before, just with a `5m` interval - note how many more candles a few days of intraday data produces.
EX 2Pull intraday 5-minute candlesNSEch05/02_intraday_history.py
Copy
```
# Intraday candles: same call, just a smaller interval like 5m.
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")

df = client.history(symbol="SBIN", exchange="NSE", interval="5m", start_date=start, end_date=end)
print("5-minute candles:", len(df))
print("First:\n", df.head(2))
print("Last:\n", df.tail(2))
```

Live output

```
5-minute candles: 300
First:
                             close     high      low  oi    open  volume
timestamp                                                              
2026-06-18 09:15:00+05:30  1030.7  1031.70  1025.05   0  1027.9  394161
2026-06-18 09:20:00+05:30  1029.5  1031.45  1028.65   0  1030.6  173356
Last:
                              close     high      low  oi     open  volume
timestamp                                                                
2026-06-23 15:20:00+05:30  1023.15  1024.25  1022.45   0  1023.20  410136
2026-06-23 15:25:00+05:30  1023.60  1025.00  1022.35   0  1023.15  358670
```

See the difference in the timestamps: daily candles are dated `2026-06-19`, while intraday candles carry a full time _and_ a timezone (`+05:30`, India Standard Time). That `09:15:00` first candle is the market open; `15:25:00` is near the close.
## Calendar days are not trading days
Here's a trap that catches every beginner. You ask for "the last 30 days" of data and get back only about 21 rows. Did something break? No - **markets don't trade every day.** Weekends are closed, and so are exchange holidays. So 30 _calendar_ days contain only ~21 _trading_ sessions.
This example asks for three different windows and counts how many actual sessions each returns.
EX 3Calendar days vs trading sessionsNSEch05/03_date_ranges.py
Copy
```
# Calendar days are not trading days -- weekends and holidays drop out.
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

today = datetime.now()
for days in [7, 30, 90]:
    start = (today - timedelta(days=days)).strftime("%Y-%m-%d")
    df = client.history(symbol="INFY", exchange="NSE", interval="D",
                        start_date=start, end_date=today.strftime("%Y-%m-%d"))
    print(f"Last {days:>3} calendar days -> {len(df)} trading sessions")
```

Live output

```
Last   7 calendar days -> 6 trading sessions
Last  30 calendar days -> 21 trading sessions
Last  90 calendar days -> 59 trading sessions
```

Heads up
Always think in **trading sessions** , not calendar days, when you need a specific amount of data. If a strategy needs 200 candles of history, asking for the last 200 _calendar_ days will leave you short - you'll get roughly 135 sessions. Request a generous window and count the rows you actually got.
The same logic plays out across intervals: the smaller the candle, the more rows you get for the identical date window. This next example fetches one ten-day window at four different intervals so you can see the row counts stack up.
EX 4More candles at smaller intervalsNSEch05/04_intervals_compare.py
Copy
```
# The smaller the interval, the more candles you get for the same window.
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")

for interval in ["D", "1h", "15m", "5m"]:
    df = client.history(symbol="TCS", exchange="NSE", interval=interval, start_date=start, end_date=end)
    print(f"{interval:4s}: {len(df):>4} candles")
```

Live output

```
D   :    7 candles
1h  :   49 candles
15m :  175 candles
5m  :  525 candles
```

## Downloading many symbols at once
A single stock is rarely enough. To compare instruments, rank a watchlist, or build a scanner, you need history for _several_ symbols. The clean pattern is a **loop** that fills a **dictionary** - one DataFrame per symbol, keyed by its name. Then you can pull up any stock's data with `data["TCS"]`.
EX 5Download a basket of symbolsNSEch05/05_multi_symbol.py
Copy
```
# Download several symbols into a dictionary of DataFrames -- one per stock.
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d")

data = {}
for sym in ["RELIANCE", "TCS", "INFY"]:
    data[sym] = client.history(symbol=sym, exchange="NSE", interval="D", start_date=start, end_date=end)

for sym, df in data.items():
    print(f"{sym:10s} last close {df['close'].iloc[-1]:>10.2f}  ({len(df)} rows)")
```

Live output

```
RELIANCE   last close    1306.00  (41 rows)
TCS        last close    2060.00  (41 rows)
INFY       last close    1029.00  (41 rows)
```

Tip
Storing each symbol's DataFrame in a dictionary is the foundation of every multi-stock study you'll do later - correlation tables, momentum rankings, pair trades. Get comfortable with `data[symbol]` now and those chapters will feel natural.
## Where the data comes from: api vs db
`client.history()` can pull from two **sources** , and you choose with the `source` argument:
  * `source="api"` - fetches fresh from your broker's servers, live. This is the default.
  * `source="db"` - reads from OpenAlgo's own local database of history it has already stored.


The local database is faster and works even if the broker's connection is down, but it only contains what's been downloaded into it. The live API is always current but slower and rate-limited. This example asks for both and compares the row counts.
EX 6Compare the api and db sourcesNSEch05/06_api_vs_db.py
Copy
```
# Two data sources: live from the broker ("api") or from stored history ("db").
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

df_api = client.history(symbol="SBIN", exchange="NSE", interval="D",
                        start_date=start, end_date=end, source="api")
print("From broker API:", len(df_api), "rows")

try:
    df_db = client.history(symbol="SBIN", exchange="NSE", interval="D",
                           start_date=start, end_date=end, source="db")
    print("From local DB  :", len(df_db), "rows")
except Exception as exc:
    print("Local DB source:", exc)
```

Live output

```
From broker API: 21 rows
From local DB  : 20 rows
```

Note
Notice the `try`/`except` around the `db` call. If the local database has no stored data for that symbol, the call could fail - and we'd rather print a clean message than crash. This is the defensive habit from Chapter 2 applied to a real, fallible data source.
## Reshaping timeframes with resample
Here's a powerful idea: you don't have to download every timeframe separately. If you have daily candles, you can **roll them up** into weekly ones yourself. If you have 5-minute candles, you can build hourly ones. This is called **resampling** , and pandas does it in a couple of lines.
The trick is telling pandas _how_ to combine each column, because you can't just average OHLCV. For a week's worth of days, the week's **open** is the _first_ day's open, the **high** is the _max_ of all the highs, the **low** is the _min_ of the lows, the **close** is the _last_ day's close, and the **volume** is the _sum_. We hand pandas exactly that recipe.
EX 7Resample daily candles to weeklyNSEch05/07_resample_weekly.py
Copy
```
# Roll daily candles up into weekly ones with pandas resample().
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")
df = client.history(symbol="RELIANCE", exchange="NSE", interval="D", start_date=start, end_date=end)

ohlc = {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
weekly = df.resample("W").agg(ohlc).dropna()

print("Daily rows:", len(df), "-> weekly rows:", len(weekly))
print(weekly.tail(3))
```

Live output

```
Daily rows: 80 -> weekly rows: 18
              open    high     low   close    volume
timestamp                                           
2026-06-14  1277.0  1300.5  1253.2  1293.0  86234040
2026-06-21  1315.3  1338.2  1303.3  1309.5  87557297
2026-06-28  1316.7  1344.9  1304.0  1306.0  28208744
```

The `"W"` in `resample("W")` means "weekly" - pandas groups the rows by calendar week and applies our aggregation recipe to each group. The exact same recipe works on intraday data: here we turn 5-minute candles into hourly ones with `resample("60min")`.
EX 8Resample 5-minute candles to hourlyNSEch05/08_resample_hourly.py
Copy
```
# The same trick intraday: turn 5-minute candles into hourly ones.
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
df = client.history(symbol="SBIN", exchange="NSE", interval="5m", start_date=start, end_date=end)

ohlc = {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
hourly = df.resample("60min").agg(ohlc).dropna()

print("5m rows:", len(df), "-> hourly rows:", len(hourly))
print(hourly.tail(3))
```

Live output

```
5m rows: 300 -> hourly rows: 28
                              open     high      low    close   volume
timestamp                                                             
2026-06-23 13:00:00+05:30  1030.35  1031.60  1023.00  1024.65  1826406
2026-06-23 14:00:00+05:30  1024.30  1029.25  1023.50  1026.55  1450825
2026-06-23 15:00:00+05:30  1026.80  1027.50  1022.35  1023.60  2437927
```

Key idea
Resampling only ever goes **up** - you can build bigger candles from smaller ones, never the reverse. You cannot recover the individual 5-minute candles from an hourly one, because that detail is gone. The practical rule: download the _smallest_ interval you'll ever need, then resample up to anything larger on demand.
## History for futures and commodities
Everything so far used NSE stocks, but `client.history()` works identically for derivatives - you just change the **symbol** and **exchange**. For an index future, use its full F&O symbol (like `NIFTY30JUN26FUT`) on the `NFO` exchange. Notice that the `oi` column, which was zero for stocks, now carries real **open interest** numbers.
EX 9Historical candles for an index futureNFOch05/09_futures_history.py
Copy
```
# History works for futures too -- just use the F&O symbol and NFO exchange.
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d")

df = client.history(symbol="NIFTY30JUN26FUT", exchange="NFO", interval="D", start_date=start, end_date=end)
print("NIFTY future sessions:", len(df))
print(df.tail(3))
```

Live output

```
NIFTY future sessions: 41
              close     high      low        oi     open   volume
timestamp                                                        
2026-06-19  24056.9  24085.0  23948.8  16483480  24019.9  3696420
2026-06-22  24123.8  24178.0  24102.0  16090685  24102.0  2096640
2026-06-23  23810.0  24155.5  23810.0  16290430  24100.0  3709225
```

And for commodities - gold, crude, silver - use the `MCX` exchange. While we're here, let's do something genuinely useful: download the history and **save it to a CSV file** so you can reuse it later without hitting the server again. A CSV (comma-separated values) is a plain-text table that opens in any spreadsheet, and `df.to_csv()` writes one in a single line.
EX 10Save MCX commodity history to CSVMCXch05/10_commodity_save_csv.py
Copy
```
# Download an MCX commodity and save it to a CSV file for later use.
import os
from datetime import datetime, timedelta
from pathlib import Path

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")

df = client.history(symbol="GOLDM03JUL26FUT", exchange="MCX", interval="15m", start_date=start, end_date=end)
print("Gold 15m candles:", len(df))

out = Path(__file__).with_name("goldm_15m.csv")
df.to_csv(out)
print("Saved to", out.name)
```

Live output

```
Gold 15m candles: 388
Saved to goldm_15m.csv
```

Tip
Saving data to CSV is how you build a local research library. Download a symbol once, save it, and your backtests can read it instantly from disk - no waiting on the network, and identical data every run, which makes your results reproducible. You can read it back later with pandas' `read_csv()`.
## Try it yourself
  * Change the interval in the first example from `"D"` to `"15m"` and shorten the window to 5 days - how many rows come back now?
  * Add `SBIN` and `HDFCBANK` to the multi-symbol basket and print each one's last close.
  * Resample the daily Reliance data to **monthly** candles by changing `"W"` to `"ME"` (month-end), and compare the row count.


## Recap
  * `client.history(symbol, exchange, interval, start_date, end_date)` returns a **DataFrame** of OHLCV candles indexed by timestamp.
  * **Intervals** run from `1m` to `D`; smaller candles mean more rows for the same window.
  * **Calendar days are not trading days** - weekends and holidays drop out, so request a generous window and count the rows you get.
  * Loop over symbols into a **dictionary** of DataFrames to study a whole basket at once.
  * The `source` argument picks fresh broker data (`"api"`) or the faster local store (`"db"`).
  * **Resample** rolls smaller candles up into bigger ones with a first/max/min/last/sum recipe - always download the smallest interval you'll need.
  * The same call works for `NFO` futures and `MCX` commodities; `df.to_csv()` saves any DataFrame for reuse.


You can now pull and reshape any instrument's history at will. Next we turn that raw price data into fast, vectorised number-crunching with NumPy - returns, volatility and the math that powers every strategy.
On this page
