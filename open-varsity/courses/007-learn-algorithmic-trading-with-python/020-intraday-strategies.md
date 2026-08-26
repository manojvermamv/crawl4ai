Chapters
Module E · Strategy Playbook - Chapter 20
# Intraday Strategies
Opening-range breakout, VWAP reversion and intraday EMA systems.
NSENFO
What you'll learn
  * ·Opening Range Breakout
  * ·VWAP mean-reversion
  * ·Intraday EMA cross
  * ·Time-based exits
  * ·MIS product
  * ·Index & stock futures


In the last chapter we held positions for days or weeks. Now we speed everything up. **Intraday trading** means every position you open is closed again before the market shuts - you carry nothing overnight. No gap-up surprises, no weekend news risk; but also no time for a slow idea to play out. You live and die inside one session.
That changes how you think. On a daily chart a single candle is a whole day. Intraday, you work with **5-minute candles** - seventy-five of them in a normal Indian equity session from 09:15 to 15:30. Patterns form and resolve in minutes, so your code has to be precise about _time_ : when the day opens, when to stop taking new trades, and when to force everything flat. This chapter builds exactly those tools, then wires them into three classic intraday systems: the **opening-range breakout** , **VWAP mean-reversion** , and an **intraday EMA crossover**.
Note
Every example here pulls **5-minute history** with `client.history(..., interval="5m")`. The returned DataFrame has a timezone-aware timestamp index in IST, which is what lets us slice by clock time and group by trading day. Run each one with `uv run python the_file.py` as always.
## The raw material: 5-minute candles
Before any strategy, get comfortable with the data. A 5-minute candle summarises five minutes of trading into one open, high, low, close and volume. Pull a couple of weeks of them and notice how many bars you get per day.
EX 1Pull 5-minute intraday candlesNSEch20/01_intraday_history.py
Copy
```
# Pull 5-minute intraday candles -- the raw material for every intraday strategy.
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")

df = client.history(symbol="SBIN", exchange="NSE", interval="5m", start_date=start, end_date=end)

# Each row is one 5-minute candle. The index is a timezone-aware timestamp (IST).
print("5m candles:", len(df), "over", df.index.normalize().nunique(), "sessions")
print("First bar of the data:", df.index[0].strftime("%Y-%m-%d %H:%M"))
print("Last bar of the data: ", df.index[-1].strftime("%Y-%m-%d %H:%M"))
print(df[["open", "high", "low", "close", "volume"]].head(3))
```

Live output

```
5m candles: 525 over 7 sessions
First bar of the data: 2026-06-15 09:15
Last bar of the data:  2026-06-23 15:25
                              open    high     low    close   volume
timestamp                                                           
2026-06-15 09:15:00+05:30  1034.00  1034.0  1026.4  1027.70  1043173
2026-06-15 09:20:00+05:30  1027.75  1029.1  1026.5  1027.15   428560
2026-06-15 09:25:00+05:30  1027.45  1029.6  1026.1  1028.90   378478
```

Intraday logic almost always runs **one day at a time** - the rules reset every morning. The cleanest way to isolate a single session is to group the DataFrame by its calendar date. `df.index.normalize()` strips the time off each timestamp, leaving just the date, which makes a perfect grouping key.
EX 2Slice out a single trading sessionNSEch20/02_one_session.py
Copy
```
# Slice out a single trading session -- intraday logic always runs day by day.
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
df = client.history(symbol="SBIN", exchange="NSE", interval="5m", start_date=start, end_date=end)

# Group by the calendar date (drop the time part) and take the most recent day.
sessions = df.groupby(df.index.normalize())
last_date = list(sessions.groups)[-1]
day = sessions.get_group(last_date)

print("Session:", last_date.strftime("%Y-%m-%d"), "with", len(day), "five-minute bars")
print("Open (first bar):", day["open"].iloc[0])
print("High of day:     ", day["high"].max())
print("Low of day:      ", day["low"].min())
print("Close (last bar):", day["close"].iloc[-1])
```

Live output

```
Session: 2026-06-23 with 75 five-minute bars
Open (first bar): 1041.0
High of day:      1045.5
Low of day:       1022.35
Close (last bar): 1023.6
```

## Strategy 1: Opening Range Breakout
Here is the intuition. In the first 15 to 30 minutes after the open, the market figures out where it wants to be - buyers and sellers fight, and a small range forms. The **opening range** is simply the high and low of that early window. The bet of an **Opening Range Breakout (ORB)** is that once price decisively _leaves_ that range, it keeps going in that direction for a while.
So the recipe is: measure the high and low of (say) the first three 5-minute bars, then watch for a later bar to close above the high (go long) or below the low (go short). `df.between_time("09:15", "09:29")` grabs exactly those opening bars, and a group-by gets us the range for every day at once.
EX 3The opening range, day by dayNSEch20/03_opening_range.py
Copy
```
# Opening Range Breakout (ORB): the high and low of the first 15 minutes.
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
df = client.history(symbol="SBIN", exchange="NSE", interval="5m", start_date=start, end_date=end)

# The first 15 minutes = the 09:15, 09:20 and 09:25 bars. between_time selects them.
opening = df.between_time("09:15", "09:29")
ranges = opening.groupby(opening.index.date).agg(or_high=("high", "max"), or_low=("low", "min"))
ranges["width"] = ranges["or_high"] - ranges["or_low"]

print("Opening range (first 15 min) per session:")
print(ranges.tail(5).round(2))
print("\nA breakout BUY triggers if a later bar closes ABOVE that day's or_high;")
print("a breakout SELL triggers if it closes BELOW that day's or_low.")
```

Live output

```
Opening range (first 15 min) per session:
            or_high   or_low  width
2026-06-17   1019.5  1014.55   4.95
2026-06-18   1031.7  1025.05   6.65
2026-06-19   1042.0  1036.65   5.35
2026-06-22   1041.6  1036.05   5.55
2026-06-23   1045.3  1037.80   7.50

A breakout BUY triggers if a later bar closes ABOVE that day's or_high;
a breakout SELL triggers if it closes BELOW that day's or_low.
```

With the range in hand, generating the actual signal for one session is just two comparisons. We look only at bars _after_ the opening window and find the first one that breaks out.
EX 4Turn the range into a breakout signalNSEch20/04_orb_signal.py
Copy
```
# Turn the opening range into an actual breakout signal for the latest session.
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
df = client.history(symbol="RELIANCE", exchange="NSE", interval="5m", start_date=start, end_date=end)

# Take the most recent session only.
last_date = df.index.normalize()[-1]
day = df[df.index.normalize() == last_date]

opening = day.between_time("09:15", "09:29")
or_high, or_low = opening["high"].max(), opening["low"].min()

# After the opening range, look for the first bar that breaks out.
after = day.between_time("09:30", "15:15")
longs = after[after["close"] > or_high]
shorts = after[after["close"] < or_low]

print(f"Session {last_date.date()}  range {or_low:.1f} - {or_high:.1f}")
if not longs.empty:
    t = longs.index[0]
    print(f"LONG breakout at {t.strftime('%H:%M')} close {longs['close'].iloc[0]:.1f}")
elif not shorts.empty:
    t = shorts.index[0]
    print(f"SHORT breakout at {t.strftime('%H:%M')} close {shorts['close'].iloc[0]:.1f}")
else:
    print("No breakout today -- price stayed inside the opening range (a quiet day).")
```

Live output

```
Session 2026-06-23  range 1323.8 - 1333.0
SHORT breakout at 11:55 close 1323.6
```

Tip
Why 15 minutes and not 5 or 60? It is a trade-off. A short window reacts faster but gets faked out by noise; a long window is more reliable but you enter later, after much of the move is gone. There is no magic number - 15 and 30 minutes are common starting points. Test it on your instrument before trusting it.
## Strategy 2: VWAP mean-reversion
**VWAP** stands for **Volume-Weighted Average Price** - the average price at which a stock has traded so far today, with each price weighted by how much volume happened there. Big institutions watch it constantly, because it tells them whether they are buying better or worse than the day's "fair" price. For us it is a magnet line: price tends to revert towards VWAP during quiet, range-bound days.
`ta.vwap` computes it for us. The key detail is the `anchor="Session"` argument, which **resets the VWAP at the start of each day** - exactly what an intraday trader wants.
EX 5VWAP, the intraday fair-value lineNSEch20/05_vwap.py
Copy
```
# VWAP -- the volume-weighted average price, the intraday fair-value line.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=8)).strftime("%Y-%m-%d")
df = client.history(symbol="INFY", exchange="NSE", interval="5m", start_date=start, end_date=end)

# anchor="Session" resets the VWAP at the start of each trading day -- exactly what
# an intraday trader wants. It is the running average price weighted by volume.
df["vwap"] = ta.vwap(df["high"], df["low"], df["close"], df["volume"], anchor="Session")
df["gap"] = (df["close"] - df["vwap"]) / df["vwap"] * 100

print(df[["close", "vwap", "gap"]].tail(6).round(3))
last = df.iloc[-1]
side = "ABOVE" if last["close"] > last["vwap"] else "BELOW"
print(f"\nPrice is {side} VWAP by {abs(last['gap']):.2f}% -- bulls control the day when price holds above VWAP.")
```

Live output

```
close      vwap    gap
timestamp                                         
2026-06-23 15:00:00+05:30  1030.9  1079.365 -4.490
2026-06-23 15:05:00+05:30  1029.7  1079.034 -4.572
2026-06-23 15:10:00+05:30  1028.0  1078.704 -4.700
2026-06-23 15:15:00+05:30  1027.8  1078.410 -4.693
2026-06-23 15:20:00+05:30  1027.1  1078.064 -4.727
2026-06-23 15:25:00+05:30  1029.0  1077.835 -4.531

Price is BELOW VWAP by 4.53% -- bulls control the day when price holds above VWAP.
```

**Mean-reversion** is the strategy of betting that an extreme snaps back to normal. Applied here: when price stretches unusually far _below_ VWAP, we buy, expecting it to pull back up towards the line. We measure "far" as a percentage gap from VWAP.
EX 6Fade stretches away from VWAPNSEch20/06_vwap_reversion.py
Copy
```
# VWAP mean-reversion: fade stretches away from VWAP, expecting a snap back.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=8)).strftime("%Y-%m-%d")
df = client.history(symbol="ICICIBANK", exchange="NSE", interval="5m", start_date=start, end_date=end)

df["vwap"] = ta.vwap(df["high"], df["low"], df["close"], df["volume"], anchor="Session")
# Distance from VWAP measured in that session's percentage terms.
df["dist"] = (df["close"] - df["vwap"]) / df["vwap"] * 100

# Reversion idea: when price is unusually FAR below VWAP, buy expecting a pullback up.
threshold = 0.40  # percent
dips = df[df["dist"] < -threshold]

print(f"5m bars more than {threshold:.2f}% below VWAP (buy-the-dip candidates):", len(dips))
print(dips[["close", "vwap", "dist"]].tail(5).round(3))
print("\nMean-reversion assumes the gap closes. It works in range days, NOT in strong trends.")
```

Live output

```
5m bars more than 0.40% below VWAP (buy-the-dip candidates): 112
                            close      vwap   dist
timestamp                                         
2026-06-16 14:40:00+05:30  1329.6  1336.431 -0.511
2026-06-16 14:45:00+05:30  1330.4  1336.311 -0.442
2026-06-23 15:15:00+05:30  1335.3  1342.340 -0.524
2026-06-23 15:20:00+05:30  1334.6  1342.276 -0.572
2026-06-23 15:25:00+05:30  1335.5  1342.236 -0.502

Mean-reversion assumes the gap closes. It works in range days, NOT in strong trends.
```

Heads up
Mean-reversion is the opposite bet to breakout, and it has a vicious failure mode: on a strong trend day, price stays far from VWAP for hours and keeps going. "Buying the dip" then means catching a falling knife. Reversion strategies need a calm, range-bound market - pair them with a filter that switches them off when the day is clearly trending.
## Strategy 3: Intraday EMA crossover
A moving average smooths price into a line. An **EMA** (Exponential Moving Average) weights recent prices more heavily, so it turns faster than a simple average. The classic momentum signal: when a **fast** EMA crosses _above_ a **slow** EMA, momentum has turned up (go long); when it crosses below, momentum has turned down (exit or go short). On 5-minute bars, 9 and 21 are popular lengths.
`ta.crossover` and `ta.crossunder` detect those exact crossing bars. Note they return a NumPy array, so we wrap the result in a pandas Series to keep it aligned with our timestamps.
EX 7An intraday EMA crossoverNSEch20/07_ema_cross.py
Copy
```
# Intraday EMA crossover: a fast EMA crossing a slow EMA is a classic momentum signal.
import os
from datetime import datetime, timedelta

import pandas as pd

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=8)).strftime("%Y-%m-%d")
df = client.history(symbol="TCS", exchange="NSE", interval="5m", start_date=start, end_date=end)

df["ema_fast"] = ta.ema(df["close"], 9)
df["ema_slow"] = ta.ema(df["close"], 21)

# crossover() returns a numpy boolean array; wrap it in a Series to align with the index.
df["buy"] = pd.Series(ta.crossover(df["ema_fast"], df["ema_slow"]), index=df.index)
df["sell"] = pd.Series(ta.crossunder(df["ema_fast"], df["ema_slow"]), index=df.index)

print("Bullish 9/21 EMA crosses:", int(df["buy"].sum()))
print("Bearish 9/21 EMA crosses:", int(df["sell"].sum()))
print("\nMost recent crossover signals:")
crosses = df[df["buy"] | df["sell"]]
for ts, row in crosses.tail(4).iterrows():
    print(f"  {ts.strftime('%m-%d %H:%M')}  {'BUY ' if row['buy'] else 'SELL'}  close {row['close']:.1f}")
```

Live output

```
Bullish 9/21 EMA crosses: 13
Bearish 9/21 EMA crosses: 13

Most recent crossover signals:
  06-19 13:50  BUY   close 2081.1
  06-22 13:00  SELL  close 2140.3
  06-23 14:25  BUY   close 2068.0
  06-23 15:05  SELL  close 2061.2
```

## Closing the day: time-based exits
This is the rule that separates intraday from everything else: **you must be flat by the close.** No matter what the strategy says, every position is squared off before the session ends. The simplest implementation is a _time-based exit_ - after a cutoff like 15:10, block new entries and force-close anything open. A time mask on the index makes this trivial.
EX 8Square off by a cutoff timeNSEch20/08_time_exit.py
Copy
```
# Time-based exit: square off everything by a cutoff time, no matter what.
import os
from datetime import datetime, timedelta

import pandas as pd

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=8)).strftime("%Y-%m-%d")
df = client.history(symbol="HDFCBANK", exchange="NSE", interval="5m", start_date=start, end_date=end)

# Entries from a 9/21 EMA cross...
df["buy"] = pd.Series(ta.crossover(ta.ema(df["close"], 9), ta.ema(df["close"], 21)), index=df.index)

# ...but force ALL positions flat after the cutoff. A time mask makes this trivial.
CUTOFF = "15:10"
square_off = df.index.indexer_between_time(CUTOFF, "15:30")
df["force_exit"] = False
df.iloc[square_off, df.columns.get_loc("force_exit")] = True

buys_after_cutoff = df[(df["buy"]) & (df["force_exit"])]
print(f"Square-off window starts at {CUTOFF} IST.")
print("New entries blocked after cutoff:", len(buys_after_cutoff), "(we ignore late signals)")
print("Bars in the square-off window per session:",
      int(df["force_exit"].sum() / df.index.normalize().nunique()))
print("\nIntraday rule: never carry an MIS position into the close -- the broker auto-squares it for you.")
```

Live output

```
Square-off window starts at 15:10 IST.
New entries blocked after cutoff: 0 (we ignore late signals)
Bars in the square-off window per session: 4

Intraday rule: never carry an MIS position into the close -- the broker auto-squares it for you.
```

## The MIS product
How does the broker know a trade is intraday? Through the **product code** you send with the order. Three matter:  
| Product  | Meaning  | Used for  |  
| --- | --- | --- |  
| **MIS**  | Margin Intraday Square-off  | Intraday trades - extra leverage, auto-closed near the session end  |  
| **CNC**  | Cash and Carry  | Delivery / overnight equity  |  
| **NRML**  | Normal  | Futures and options carried overnight  |  
**MIS** is the intraday product. It gives you more leverage (you can take a bigger position for the same cash) precisely _because_ the broker will force it closed the same day, capping its overnight risk. If you forget to square off, the broker does it for you near the close. Below we place a simulated MIS order on an MCX commodity (MCX trades into the evening, so the order is accepted even after the equity market has shut).
EX 9Place an intraday MIS orderMCXch20/09_mis_order.py
Copy
```
# The MIS product: intraday margin orders that auto-square-off before the close.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# product="MIS" tells the broker this is an intraday trade. It gives extra leverage
# but the position is force-closed near the session close. We use an MCX commodity
# future here because MCX trades into the evening, so this MIS order is accepted
# even after the equity market has shut. (Server is in analyze mode -- it is simulated.)
resp = client.placeorder(
    strategy="Intraday ORB",
    symbol="GOLDM03JUL26FUT",
    action="BUY",
    exchange="MCX",
    price_type="MARKET",
    product="MIS",      # MIS = intraday;  CNC = delivery;  NRML = F&O carry
    quantity=1,
)

print("Order status:", resp.get("status"))
print("Order id     :", resp.get("orderid"))
print("\nProduct codes you will use intraday:")
print("  MIS  -> intraday, higher leverage, auto square-off (this strategy)")
print("  CNC  -> delivery / overnight equity")
print("  NRML -> futures & options carried overnight")
print("\nNote: equity MIS orders are blocked after 15:15 IST -- the broker enforces square-off for you.")
```

Live output

```
Order status: success
Order id     : 26062327903016

Product codes you will use intraday:
  MIS  -> intraday, higher leverage, auto square-off (this strategy)
  CNC  -> delivery / overnight equity
  NRML -> futures & options carried overnight

Note: equity MIS orders are blocked after 15:15 IST -- the broker enforces square-off for you.
```

Key idea
The exchange itself enforces intraday discipline. Try to place an _equity_ MIS order after the square-off time (around 15:15 IST) and the broker rejects it outright - you cannot accidentally open a fresh intraday position that has no time left to close. This is a safety rail, not an inconvenience.
## Putting it together: a backtested intraday system
Finally, let's _test_ an intraday idea instead of trusting it. We take the 9/21 EMA crossover, add a daily square-off so nothing is held overnight, and run it through **VectorBT** on the NIFTY index future (an NFO instrument). One subtlety: intraday data has overnight gaps between sessions, and VectorBT's date-frequency logic stumbles on them - so we hand it a plain integer index instead. The result is deliberately unglamorous, which is the lesson.
EX 10Backtest an intraday system with VectorBTNFOch20/10_futures_orb_backtest.py
Copy
```
# Backtest an intraday EMA system on the NIFTY future with VectorBT.
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
start = (datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d")


def hist():
    for _ in range(3):
        d = client.history(symbol="NIFTY30JUN26FUT", exchange="NFO", interval="5m",
                           start_date=start, end_date=end)
        if isinstance(d, pd.DataFrame) and "close" in d:
            return d
        time.sleep(1)
    raise RuntimeError(f"Could not fetch history: {d}")


df = hist()
close = df["close"]
entries = pd.Series(ta.crossover(ta.ema(close, 9), ta.ema(close, 21)), index=close.index)
exits = pd.Series(ta.crossunder(ta.ema(close, 9), ta.ema(close, 21)), index=close.index)

# Square off every position on the last bar of each session (no overnight risk).
day = pd.Series(df.index.normalize(), index=df.index)
exits = exits | (day != day.shift(-1))

import vectorbt as vbt

# Reset to a simple integer index so VectorBT ignores the overnight gaps between sessions.
pf = vbt.Portfolio.from_signals(
    close.reset_index(drop=True), entries.reset_index(drop=True), exits.reset_index(drop=True),
    init_cash=500000, fees=0.0003,
)
print("NIFTY future intraday EMA 9/21 (5m, square-off each day)")
print("Total return :", round(float(pf.total_return()) * 100, 2), "%")
print("Trades       :", int(pf.trades.count()))
print("Win rate     :", round(float(pf.trades.win_rate()) * 100, 1), "%")
print("\nA losing result on a few weeks of data is normal -- intraday edges are thin and costs bite.")
```

Live output

```
NIFTY future intraday EMA 9/21 (5m, square-off each day)
Total return : -2.08 %
Trades       : 32
Win rate     : 28.1 %

A losing result on a few weeks of data is normal -- intraday edges are thin and costs bite.
```

Heads up
Intraday edges are thin and **costs are brutal**. You trade often, so brokerage, exchange fees and slippage stack up fast - a strategy that looks profitable on paper can bleed out once you subtract realistic costs. Always backtest with fees included (we used `fees=0.0003`), and treat any intraday system that ignores costs as fiction.
## Try it yourself
  * Change the opening-range window in `03_opening_range.py` from the first 15 minutes (`"09:15"` to `"09:29"`) to the first 30 minutes and see how the ranges widen.
  * In the VWAP reversion example, swap `ICICIBANK` for a more volatile stock and adjust the `threshold` - does it find more or fewer dips?
  * Move the square-off cutoff in `08_time_exit.py` earlier to `"14:45"` and rerun the EMA backtest with that rule. Does avoiding the last hour help or hurt?


## Recap
  * **Intraday** means flat by the close - no overnight risk, but no patience either. You work in 5-minute candles and slice the day by clock time.
  * The **Opening Range Breakout** trades a decisive move out of the first 15-30 minutes' high/low.
  * **VWAP** is the volume-weighted fair-value line; **mean-reversion** fades stretches away from it - but only on range days.
  * An **EMA crossover** (fast over slow) is a simple momentum trigger; `ta.crossover`/`crossunder` find the exact bars.
  * A **time-based exit** and the **MIS** product enforce the square-off discipline; the exchange blocks late intraday entries for you.
  * Intraday edges are thin and **costs dominate** - always backtest with fees in VectorBT before believing a result.


Next we step into market-neutral territory: instead of betting on a single stock's direction, we trade the _relationship_ between two stocks with pair trading and statistical arbitrage.
On this page
