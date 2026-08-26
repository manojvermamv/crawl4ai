Chapters
Module A · Foundations - Chapter 07
# Pandas for Traders
DataFrames, rolling windows, resampling and group-bys - the workhorse of market analysis.
NSEMCX
What you'll learn
  * ·Series & DataFrame on OHLCV
  * ·Indexing & slicing by date
  * ·Rolling windows
  * ·Resample to higher TF
  * ·groupby aggregations
  * ·Returns & drawdown


If NumPy gave you fast arrays of numbers, Pandas gives you something that feels far more natural to a trader: a **table**. Rows of dates down the side, columns of open, high, low, close and volume across the top - exactly how you already picture market data in your head. Every time you called `client.history()` in the earlier chapters, what came back was a Pandas table. This chapter is about actually _working_ with it.
Pandas is the single most-used tool in this entire series. Backtests, indicators, scanners, performance reports - they all stand on the two ideas you'll meet here: the **Series** (one column) and the **DataFrame** (the whole table). By the end you'll be slicing data by date, computing returns and moving averages, rolling daily candles up to weekly, grouping by weekday, and measuring drawdown - the real work of market analysis, in a handful of lines each.
Note
Run every example as you read, and poke at it. Change `RELIANCE` to a stock you follow, widen the date window, print an extra column. Pandas rewards experimentation - you learn its shortcuts by trying them. Run any file with `uv run python the_file.py`, as set up in Chapter 1.
## The DataFrame and the Series
A **DataFrame** is a table: rows and named columns, like a spreadsheet that Python can compute on. A **Series** is a single column pulled out of that table - one labelled list of values. When `client.history()` returns data, the columns are `close high low oi open volume` and the rows are labelled by a `timestamp` **index** - the special column Pandas uses to identify each row (here, the date of each candle).
Three attributes tell you almost everything about a fresh table: `.shape` (how many rows and columns), `.columns` (their names), and `.head()` / `.tail()` (a peek at the top or bottom rows). Get in the habit of printing these the moment data arrives - it's how you catch a wrong symbol or an empty download before it wastes your time.
EX 1Meet the DataFrame and its indexNSEch07/01_dataframe_basics.py
Copy
```
# A DataFrame is a table; a Series is one of its columns. Meet both.
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=40)).strftime("%Y-%m-%d")

df = client.history(symbol="RELIANCE", exchange="NSE", interval="D", start_date=start, end_date=end)

print("Type      :", type(df).__name__)        # DataFrame -- the whole table
print("Shape     :", df.shape)                  # (rows, columns)
print("Columns   :", df.columns.tolist())       # the column labels
print("Index name:", df.index.name)             # the timestamp index
print("\nFirst 3 rows:")
print(df.head(3))
```

Live output

```
Type      : DataFrame
Shape     : (28, 6)
Columns   : ['close', 'high', 'low', 'oi', 'open', 'volume']
Index name: timestamp

First 3 rows:
             close    high     low  oi    open    volume
timestamp                                               
2026-05-14  1361.8  1378.0  1358.4   0  1365.2  17303059
2026-05-15  1336.4  1364.8  1329.2   0  1356.8  19976192
2026-05-18  1335.9  1342.0  1318.7   0  1334.0  13022473
```

Key idea
The **index** is the row labels - here, the trading dates. It is not an ordinary column; it's how Pandas finds rows. Because our index is made of timestamps, we get date-aware superpowers for free: slicing by date, resampling to weekly, grouping by weekday. Keep the timestamp as the index and life is easy.
## Selecting columns
To grab one column, put its name in square brackets: `df["close"]`. That hands you back a **Series** - and a Series comes loaded with instant summaries: `.max()`, `.min()`, `.mean()`, and `.iloc[-1]` for the most recent value (`iloc` means "index by position", so `-1` is the last row). To grab several columns at once, pass a _list_ of names inside the brackets - `df[["high", "low"]]` - and you get back a smaller DataFrame.
EX 2Select one column and severalNSEch07/02_select_columns.py
Copy
```
# Pull single columns (Series) and several columns (a smaller DataFrame).
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=40)).strftime("%Y-%m-%d")
df = client.history(symbol="TCS", exchange="NSE", interval="D", start_date=start, end_date=end)

close = df["close"]                  # one column -> a Series
print("close is a", type(close).__name__)
print("Latest close :", close.iloc[-1])      # iloc[-1] = last value by position
print("Highest close:", close.max())
print("Average close:", round(close.mean(), 2))

hl = df[["high", "low"]]             # two columns -> a DataFrame
print("\nHigh/Low table (last 3 rows):")
print(hl.tail(3))
```

Live output

```
close is a Series
Latest close : 2060.0
Highest close: 2446.9
Average close: 2232.11

High/Low table (last 3 rows):
              high     low
timestamp                 
2026-06-19  2138.0  2059.9
2026-06-22  2157.0  2121.0
2026-06-23  2114.0  2055.0
```

Heads up
Watch the brackets. `df["close"]` (single brackets, one name) gives a Series. `df[["close"]]` (double brackets) gives a one-column DataFrame. They print differently and behave differently. When you want a column to compute on, you almost always want the single-bracket Series.
## Slicing by date with .loc
Because the index is dates, you can ask for a _range_ of dates directly. `.loc` is the label-based selector: `df.loc["2026-05-01":]` returns every row from the 1st of May onward; `df.loc["2026-05-01":"2026-05-31"]` gives just that month. No filtering, no loops - you describe the window in plain dates and Pandas finds it. `.loc` also reads a single row by its exact label.
This is the workhorse for "how did this behave last month?" questions. Notice we build the date string from `datetime` and `timedelta` so the example stays correct no matter when you run it.
EX 3Slice rows by date with .locNSEch07/03_slice_by_date.py
Copy
```
# Slice rows by date with .loc -- the timestamp index makes this effortless.
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now()
start = end - timedelta(days=90)
df = client.history(symbol="INFY", exchange="NSE", interval="D",
                    start_date=start.strftime("%Y-%m-%d"), end_date=end.strftime("%Y-%m-%d"))

# Last 30 calendar days as a date string -- .loc selects every row from there on.
last_month = (end - timedelta(days=30)).strftime("%Y-%m-%d")
recent = df.loc[last_month:]
print(f"Rows since {last_month}:", len(recent))
print("Close range in window:", recent["close"].min(), "to", recent["close"].max())

# .loc also reads a single row by its exact index label.
one_row = df.loc[df.index[-1]]
print("\nMost recent session:")
print(one_row)
```

Live output

```
Rows since 2026-05-24: 21
Close range in window: 1029.0 to 1243.9

Most recent session:
close         1029.0
high          1055.3
low           1026.0
oi               0.0
open          1053.8
volume    19209317.0
Name: 2026-06-23 00:00:00, dtype: float64
```

## Rolling windows: the moving average
A **moving average** smooths out the daily noise so you can see the trend. `.rolling(window=20)` slides a 20-row window down the column, and `.mean()` averages each window - giving you the 20-day simple moving average (**SMA**). Assign it back as a new column and it lines up perfectly with the dates it belongs to.
The first 19 values come out as `NaN` ("not a number") simply because there aren't yet 20 days to average - that's expected, not a bug. Comparing the close to its moving average is one of the oldest trend reads there is: above the average, the trend is up; below it, down.
EX 4Rolling moving averagesNSEch07/04_rolling_average.py
Copy
```
# .rolling() slides a window across the data -- the basis of every moving average.
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")
df = client.history(symbol="HDFCBANK", exchange="NSE", interval="D", start_date=start, end_date=end)

df["sma20"] = df["close"].rolling(window=20).mean()   # 20-day simple moving average
df["sma50"] = df["close"].rolling(window=50).mean()   # 50-day simple moving average

print(df[["close", "sma20", "sma50"]].tail(4))

# A classic read: is price trading above its 20-day average?
last = df.iloc[-1]
trend = "above" if last["close"] > last["sma20"] else "below"
print(f"\nClose {last['close']} is {trend} the 20-day average {round(last['sma20'], 2)}")
```

Live output

```
close     sma20    sma50
timestamp                           
2026-06-18  799.0  761.5000  774.838
2026-06-19  779.8  762.5325  774.994
2026-06-22  786.4  763.5125  774.400
2026-06-23  772.9  762.8150  773.904

Close 772.9 is above the 20-day average 762.82
```

Tip
`.rolling()` isn't just for averages. Swap `.mean()` for `.max()` to get a rolling high (the heart of a breakout system), `.min()` for a rolling low, or `.std()` for rolling volatility. The window slides; you choose what to compute inside it.
## Percentage returns with .pct_change()
Prices tell you the level; **returns** tell you the move. A daily return is simply today's close divided by yesterday's, minus one - and `.pct_change()` does exactly that for the whole column in one call. The very first value is `NaN` (there's no prior day to compare against), which is why we count up-days only where the return exists.
Returns are the universal language of performance: they let you compare a 3000-rupee stock with a 200-rupee one on equal terms, and they're the input to almost every statistic you'll compute later - average return, volatility, Sharpe ratio, and more.
EX 5Daily returns with pct_changeNSEch07/05_pct_change_returns.py
Copy
```
# .pct_change() turns a price column into daily percentage returns.
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
df = client.history(symbol="ICICIBANK", exchange="NSE", interval="D", start_date=start, end_date=end)

df["ret"] = df["close"].pct_change()        # today/yesterday - 1, as a fraction
df["ret_pct"] = (df["ret"] * 100).round(2)  # same thing as a readable percentage

print(df[["close", "ret_pct"]].tail(5))

up_days = (df["ret"] > 0).sum()             # boolean True counts as 1
print("\nUp days     :", int(up_days), "of", df["ret"].notna().sum())
print("Best day    :", round(df["ret"].max() * 100, 2), "%")
print("Worst day   :", round(df["ret"].min() * 100, 2), "%")
print("Average day :", round(df["ret"].mean() * 100, 3), "%")
```

Live output

```
close  ret_pct
timestamp                  
2026-06-17  1336.8     0.19
2026-06-18  1342.3     0.41
2026-06-19  1346.5     0.31
2026-06-22  1352.4     0.44
2026-06-23  1335.5    -1.25

Up days     : 30 of 58
Best day    : 5.11 %
Worst day   : -2.26 %
Average day : 0.112 %
```

## Resampling to a higher timeframe
**Resampling** changes the candle size. You downloaded daily data, but you want a weekly view - `.resample("W")` regroups the rows into weekly buckets, and `.agg()` tells Pandas how to combine each column: the week's **open** is the _first_ value, its **high** is the _max_ , its **low** is the _min_ , its **close** is the _last_ , and its **volume** is the _sum_. That recipe is the correct way to build any higher timeframe from a lower one.
Here we do it on an MCX commodity - gold - to show the technique works identically across exchanges. Use `"W"` for weekly, `"ME"` for month-end, `"QE"` for quarter-end.
EX 6Resample daily to weekly (MCX gold)MCXch07/06_resample_weekly.py
Copy
```
# .resample() rolls daily candles up to weekly -- here on an MCX commodity.
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")
df = client.history(symbol="GOLDM03JUL26FUT", exchange="MCX", interval="D", start_date=start, end_date=end)

# Each weekly candle: first open, highest high, lowest low, last close, summed volume.
rules = {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
weekly = df.resample("W").agg(rules).dropna()

print("Daily rows:", len(df), "-> weekly rows:", len(weekly))
print(weekly.tail(4))
```

Live output

```
Daily rows: 86 -> weekly rows: 18
              open    high     low   close  volume
timestamp                                         
2026-06-07  157987  158237  153023  153712  160436
2026-06-14  153043  153685  144328  148719  219886
2026-06-21  151061  151930  143688  145221  171291
2026-06-28  145699  147124  143518  144366   53278
```

Key idea
Never resample OHLC with a plain `.mean()` - averaging an open price is meaningless. Always use the first / max / min / last / sum recipe above. Getting this right is what separates a real weekly candle from a misleading blur.
## Grouping with .groupby()
`.groupby()` splits the data into buckets that share a label, then computes one number per bucket. The classic trader's question: _does the day of the week matter?_ We tag each row with its weekday name (`.index.day_name()` reads it straight off the timestamp), then `groupby("weekday")["ret"].mean()` gives the average return for Mondays, Tuesdays, and so on.
Treat the result as curiosity, not gospel - a few months of data is far too little to trade a "best weekday" on. But the _technique_ is everything: group by month, by hour of the day, by whether RSI was high or low, and you have the engine behind every seasonal and conditional study in this series.
EX 7Average return by weekdayNSEch07/07_groupby_weekday.py
Copy
```
# .groupby() answers "which weekday has the best average return?"
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=200)).strftime("%Y-%m-%d")
df = client.history(symbol="SBIN", exchange="NSE", interval="D", start_date=start, end_date=end)

df["ret"] = df["close"].pct_change()
df["weekday"] = df.index.day_name()        # Monday, Tuesday, ... from the timestamp

# Group the returns by weekday and average each group.
by_day = df.groupby("weekday")["ret"].mean() * 100
order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
by_day = by_day.reindex(order)             # keep the natural week order

print("Average daily return by weekday (%):")
print(by_day.round(3))
print("\nBest weekday on average:", by_day.idxmax())
```

Live output

```
Average daily return by weekday (%):
weekday
Monday       0.030
Tuesday      0.309
Wednesday    0.569
Thursday    -0.074
Friday      -0.394
Name: ret, dtype: float64

Best weekday on average: Wednesday
```

## Cumulative returns with .cumprod()
A single day's return is small; what compounds it into wealth is _stringing them together_. If you make 1% then lose 2%, your money is multiplied by `1.01 × 0.98`. `.cumprod()` (cumulative product) does that running multiplication down the whole column, turning a list of daily returns into a **growth curve** - the value of one rupee invested on day one. Multiply by your starting capital and you have an equity curve.
This is the literal definition of buy-and-hold performance, and it's the same calculation that will power every backtest equity curve later - only there the returns will be your _strategy's_ , not the raw stock's.
EX 8Compound returns into a growth curveNSEch07/08_cumulative_returns.py
Copy
```
# Chain daily returns into a growth curve with .cumprod().
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")
df = client.history(symbol="RELIANCE", exchange="NSE", interval="D", start_date=start, end_date=end)

df["ret"] = df["close"].pct_change().fillna(0)

# Each day multiplies the running balance by (1 + that day's return).
df["growth"] = (1 + df["ret"]).cumprod()       # 1.0 = starting value
df["equity"] = 100000 * df["growth"]           # what 1,00,000 would have become

print(df[["close", "growth", "equity"]].tail(4).round(2))

total = (df["growth"].iloc[-1] - 1) * 100
print(f"\nBuy-and-hold over {len(df)} sessions: {round(total, 2)}%")
```

Live output

```
close  growth    equity
timestamp                           
2026-06-18  1328.1    0.85  85178.30
2026-06-19  1309.5    0.84  83985.38
2026-06-22  1326.5    0.85  85075.68
2026-06-23  1306.0    0.84  83760.90

Buy-and-hold over 120 sessions: -16.24%
```

## Running max and drawdown
A growing equity curve hides the suffering along the way. **Drawdown** measures that suffering: how far below its previous peak the price (or your account) is right now, as a percentage. The trick is `.cummax()` - the running maximum, the highest value seen _so far_. Today's close divided by that running peak, minus one, is today's drawdown. The minimum of that column is the worst peak-to-trough fall over the period.
Drawdown is arguably the most important risk number there is. A strategy that doubles your money but takes you through a 60% drawdown is one most people abandon at the bottom. We compute it here on MCX gold; later it becomes the backbone of performance reporting.
EX 9Running max and drawdown (MCX gold)MCXch07/09_drawdown.py
Copy
```
# Running max with .cummax() gives you drawdown -- the pain of every dip.
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")
df = client.history(symbol="GOLDM03JUL26FUT", exchange="MCX", interval="D", start_date=start, end_date=end)

df["peak"] = df["close"].cummax()                       # highest close seen so far
df["drawdown"] = (df["close"] / df["peak"] - 1) * 100   # % below that peak today

print(df[["close", "peak", "drawdown"]].tail(4).round(2))
print("\nDeepest drawdown:", round(df["drawdown"].min(), 2), "%")
print("On date         :", df["drawdown"].idxmin().date())
```

Live output

```
close    peak  drawdown
timestamp                           
2026-06-18  147424  198661    -25.79
2026-06-19  145221  198661    -26.90
2026-06-22  146125  198661    -26.45
2026-06-23  144366  198661    -27.33

Deepest drawdown: -27.7 %
On date         : 2026-03-24
```

## Combining two symbols into one table
Real analysis rarely involves one symbol. To compare two, you download each one's close as a Series and stitch them together with `pd.concat(..., axis=1)`. The magic is **alignment** : Pandas matches the two Series on their shared timestamp index, so the same calendar date always lines up on the same row, even if one symbol had a missing session. A `.dropna()` then keeps only the dates both have.
Once two closes sit in one table, the whole toolkit opens up - here we take each one's returns and ask how tightly they move together with `.corr()` (correlation). Aligned price tables like this are the starting point for pairs trading, relative strength, and portfolio work down the line.
EX 10Combine two symbols' closesNSEch07/10_combine_symbols.py
Copy
```
# Combine two symbols' closes into one aligned DataFrame, then compare them.
import os
from datetime import datetime, timedelta

import pandas as pd
from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")


def close_of(sym):
    d = client.history(symbol=sym, exchange="NSE", interval="D", start_date=start, end_date=end)
    return d["close"]


# pd.concat lines the two Series up on their shared timestamp index.
prices = pd.concat({"TCS": close_of("TCS"), "INFY": close_of("INFY")}, axis=1).dropna()
print(prices.tail(3))

# Correlation of daily returns -- do these two IT names move together?
rets = prices.pct_change().dropna()
print("\nReturn correlation:", round(rets["TCS"].corr(rets["INFY"]), 3))
```

Live output

```
TCS    INFY
timestamp                 
2026-06-19  2125.0  1051.4
2026-06-22  2127.8  1065.4
2026-06-23  2060.0  1029.0

Return correlation: 0.818
```

## Summarising with .describe()
When you meet a new column, `.describe()` is the fastest way to know it. In one call it reports the count, mean, standard deviation (a measure of spread - for returns, this _is_ volatility), the minimum and maximum, and the quartiles. Run it on a return column and you get an instant character sketch: typical day, best day, worst day, and how jumpy the stock is.
We finish by scaling the daily standard deviation up to an **annualised volatility** - multiply by the square root of about 252 trading days - the standard way to quote how volatile an instrument is per year.
EX 11Summarise a column with describeNSEch07/11_describe_stats.py
Copy
```
# .describe() and friends summarise a whole column in one line.
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")
df = client.history(symbol="HDFCBANK", exchange="NSE", interval="D", start_date=start, end_date=end)

df["ret_pct"] = df["close"].pct_change() * 100      # daily returns in percent

# describe() gives count, mean, std (volatility), min, quartiles and max at once.
print("Daily return summary (%):")
print(df["ret_pct"].describe().round(3))

# Annualised volatility: daily std (in %) scaled by the square root of ~252 trading days.
ann_vol = df["ret_pct"].std() * (252 ** 0.5)
print("\nAnnualised volatility:", round(ann_vol, 1), "%")
```

Live output

```
Daily return summary (%):
count    79.000
mean     -0.208
std       1.884
min      -5.320
25%      -1.588
50%      -0.266
75%       0.985
max       5.712
Name: ret_pct, dtype: float64

Annualised volatility: 29.9 %
```

## Try it yourself
  * In the rolling-average example, add a 200-day average and check whether the close sits above or below it - the most-watched line in all of trend trading.
  * Change the resample rule in the weekly example from `"W"` to `"ME"` (month-end) and compare how many candles you get.
  * In the combine-symbols example, swap one IT name for a bank like `HDFCBANK` and see whether the return correlation rises or falls.


## Recap
  * A **DataFrame** is the table; a **Series** is one column. `client.history()` hands you a DataFrame indexed by `timestamp`.
  * Select with `df["close"]` (Series) or `df[["high", "low"]]` (DataFrame); summarise with `.mean()`, `.max()`, `.iloc[-1]`.
  * `.loc["date":]` slices by date; `.rolling(window=n).mean()` builds moving averages; `.pct_change()` gives returns.
  * `.resample("W").agg(...)` rolls candles up a timeframe - always first/max/min/last/sum, never a plain mean.
  * `.groupby()` answers "by category" questions; `.cumprod()` compounds returns into a growth curve.
  * `.cummax()` powers drawdown, `pd.concat(axis=1)` aligns symbols by date, and `.describe()` profiles any column in one line.


Next we turn these numbers into pictures. Chapter 8 takes the very same DataFrames and draws them - price lines, return histograms, indicator overlays and candlesticks - with Matplotlib.
On this page
