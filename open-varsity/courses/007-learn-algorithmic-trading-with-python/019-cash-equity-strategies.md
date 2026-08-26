Chapters
Module E · Strategy Playbook - Chapter 19
# Cash & Equity Strategies
Delivery-style trend following and momentum ranking on equities.
NSE
What you'll learn
  * ·Golden-cross trend
  * ·Momentum ranking
  * ·Donchian breakout
  * ·Position vs CNC
  * ·Equity curve preview
  * ·Universe rotation


So far you've built signals and scanned the market with them. Now we assemble those pieces into actual **strategies** - complete rules for what to buy, when to sell, and how to hold. This chapter stays in the world of **cash equities** : ordinary shares of companies like Reliance or Infosys, bought for _delivery_ and held for days, weeks or months. No leverage, no expiry, no overnight square-off - the patient end of trading, and the right place to learn strategy design before the faster styles in later chapters.
We'll build three classic delivery systems - a golden-cross trend follower, a momentum rotation across a universe, and a Donchian channel breakout - and preview each one's equity curve so you can see, roughly, whether it would have made money. That preview is a hand-rolled backtest; we keep it simple here and hand the job to the proper tool, VectorBT, in Chapter 26. We'll also settle the question that trips up every new equity trader: **CNC versus MIS**.

```
from openalgo import api, ta

```

## The golden cross
The most famous trend signal in all of investing: the **golden cross** , when the 50-day simple moving average rises above the 200-day. It says the medium-term trend has overtaken the long-term one - the market has turned up. Its opposite, the 50 falling below the 200, is the **death cross**. Whole trend-following systems are built on nothing more.
EX 1Read the golden / death cross regimeNSEch19/01_golden_cross.py
Copy
```
# The golden cross: 50-day SMA crossing above the 200-day SMA. A classic trend filter.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# 200-day SMA needs a long history -- ~400 calendar days gives plenty of bars.
end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=400)).strftime("%Y-%m-%d")
df = client.history(symbol="RELIANCE", exchange="NSE", interval="D", start_date=start, end_date=end)

close = df["close"]
sma50 = ta.sma(close, 50)
sma200 = ta.sma(close, 200)

regime = "BULLISH (golden cross)" if sma50.iloc[-1] > sma200.iloc[-1] else "BEARISH (death cross)"
print("Latest close :", round(float(close.iloc[-1]), 2))
print("SMA50  :", round(float(sma50.iloc[-1]), 2))
print("SMA200 :", round(float(sma200.iloc[-1]), 2))
print("Current regime:", regime)
```

Live output

```
Latest close : 1306.0
SMA50  : 1347.39
SMA200 : 1420.74
Current regime: BEARISH (death cross)
```

Note
The 200-day average needs 200 _trading_ days of data before it produces a single value - roughly ten calendar months. That's why these examples request around 400 calendar days of history. Ask for too little and `ta.sma(close, 200)` returns nothing but `NaN` (not-a-number) at the end, and your strategy silently does nothing.
The regime check above tells you where you stand _today_. To backtest, you need the _dated moments_ the cross actually happened - and that's exactly the `crossover` / `crossunder` pair from Chapter 17.
EX 2Dated golden-cross entries and exitsNSEch19/02_golden_cross_signals.py
Copy
```
# Turn the golden/death cross into dated entry and exit signals.
import os
from datetime import datetime, timedelta

import pandas as pd
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=600)).strftime("%Y-%m-%d")
df = client.history(symbol="HDFCBANK", exchange="NSE", interval="D", start_date=start, end_date=end)

close = df["close"]
sma50, sma200 = ta.sma(close, 50), ta.sma(close, 200)

golden = pd.Series(ta.crossover(sma50, sma200), index=df.index)   # 50 crosses above 200 -> buy
death = pd.Series(ta.crossunder(sma50, sma200), index=df.index)   # 50 crosses below 200 -> exit

print("Golden crosses:", int(golden.sum()), "| Death crosses:", int(death.sum()))
events = pd.DataFrame({"close": close, "golden": golden, "death": death})
print(events[golden | death].tail(6))
```

Live output

```
Golden crosses: 0 | Death crosses: 1
            close  golden  death
timestamp                       
2026-01-28  932.7   False   True
```

## Previewing an equity curve
A signal is a hypothesis. An **equity curve** is how you check it: take a starting stake of 1.0 and watch how it grows (or shrinks) if you'd followed the rule. The recipe is short and you'll use it constantly:
  1. Build an in-position flag with `ta.flip(buy, sell)` - `1` while you hold, `0` while flat.
  2. Take daily returns with `close.pct_change()`.
  3. Multiply returns by the flag **shifted one bar** (`.shift(1)`) - you only earn a day's return if you were already in the trade at yesterday's close.
  4. Compound the result with `(1 + strat_ret).cumprod()`.

EX 3A hand-rolled equity-curve previewNSEch19/03_equity_curve_preview.py
Copy
```
# A quick equity-curve preview from signals -- no VectorBT yet (that's Chapter 26).
import os
from datetime import datetime, timedelta

import pandas as pd
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=400)).strftime("%Y-%m-%d")
df = client.history(symbol="ICICIBANK", exchange="NSE", interval="D", start_date=start, end_date=end)

close = df["close"]
# A 20/50 EMA cross trades more often than 50/200 -- handy for showing a real curve.
fast, slow = ta.ema(close, 20), ta.ema(close, 50)
buy = pd.Series(ta.crossover(fast, slow), index=df.index)
sell = pd.Series(ta.crossunder(fast, slow), index=df.index)

# Hold a long while flip() is on; shift(1) so we earn TOMORROW's return, not today's.
position = pd.Series(ta.flip(buy, sell), index=df.index).astype(int)
daily_ret = close.pct_change().fillna(0)
strat_ret = daily_ret * position.shift(1).fillna(0)

strat_curve = (1 + strat_ret).cumprod()
buyhold_curve = (1 + daily_ret).cumprod()
print("Strategy   total return: {:.1f}%".format((strat_curve.iloc[-1] - 1) * 100))
print("Buy & hold total return: {:.1f}%".format((buyhold_curve.iloc[-1] - 1) * 100))
print("Days in the market:", int(position.sum()), "of", len(position))
print("Final equity on 1.0 start:", round(float(strat_curve.iloc[-1]), 3))
```

Live output

```
Strategy   total return: -15.5%
Buy & hold total return: -7.8%
Days in the market: 56 of 273
Final equity on 1.0 start: 0.845
```

Heads up
This preview ignores brokerage, slippage and taxes, so its numbers are optimistic - treat them as a smell test, not a verdict. A strategy that loses _before_ costs will lose more _after_ them. Chapter 26 redoes this properly with VectorBT and realistic costs; until then, use the preview only to sanity-check that a rule does roughly what you intended.
Notice the example compares the strategy to simple **buy-and-hold**. That comparison is the honest benchmark for any equity system: if you can't beat just owning the stock, the extra complexity isn't earning its keep.
## Momentum ranking across a universe
Trend-following picks a side on _one_ stock. **Momentum rotation** asks a sharper question across _many_ : which names are strongest right now, and hold those. You rank the universe by its recent return - say the last 60 trading days - buy the leaders, and re-rank periodically, rotating out of laggards. It's the strategy logic behind countless equity funds, and it's a direct descendant of the ranking table you built in Chapter 18.
EX 4Rank a universe by momentumNSEch19/04_momentum_ranking.py
Copy
```
# Momentum ranking: sort a universe by N-day return and buy the leaders.
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
start = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")
LOOKBACK = 60  # trading-bar momentum window


def daily(sym):
    df = client.history(symbol=sym, exchange="NSE", interval="D", start_date=start, end_date=end)
    return df if isinstance(df, pd.DataFrame) and not df.empty else None


rows = []
for sym in universe:
    df = daily(sym)
    if df is None or len(df) <= LOOKBACK:
        continue
    close = df["close"]
    mom = (close.iloc[-1] / close.iloc[-1 - LOOKBACK] - 1) * 100
    rows.append({"symbol": sym, "momentum_%": round(float(mom), 2)})

ranked = pd.DataFrame(rows).sort_values("momentum_%", ascending=False).reset_index(drop=True)
ranked.index += 1
print(f"Ranked by {LOOKBACK}-bar momentum. A rotation would hold the top 3:")
print(ranked.to_string())
print("\nTop 3 to hold this month:", list(ranked["symbol"].head(3)))
```

Live output

```
Ranked by 60-bar momentum. A rotation would hold the top 3:
       symbol  momentum_%
1          LT       24.75
2    AXISBANK       16.01
3   KOTAKBANK       12.72
4   ICICIBANK        9.23
5      MARUTI        8.70
6    HDFCBANK        3.86
7         ITC        2.56
8        SBIN       -0.80
9       WIPRO       -7.01
10   RELIANCE       -7.23
11        TCS      -13.58
12       INFY      -16.36

Top 3 to hold this month: ['LT', 'AXISBANK', 'KOTAKBANK']
```

The output is a leaderboard. A real rotation would hold the top few names, then re-run this each month and swap any that have dropped off the top. Simple, mechanical, and completely free of opinion - which is rather the point.
## Donchian channel breakout
The **Donchian channel** plots the highest high and lowest low of the last N days as an upper and lower band. The strategy is pure breakout: buy when price closes above the upper band (a new N-day high), exit when it closes below the lower band. It's the skeleton of one of the most famous trend systems ever traded, and `ta.donchian` builds the bands for you.
EX 5Read a Donchian breakout signalNSEch19/05_donchian_breakout.py
Copy
```
# Donchian channel breakout: buy a close above the 20-day high, exit below the 20-day low.
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
df = client.history(symbol="INFY", exchange="NSE", interval="D", start_date=start, end_date=end)

# donchian returns three Series: upper (highest high), middle, lower (lowest low).
upper, middle, lower = ta.donchian(df["high"], df["low"], period=20)

close = df["close"].iloc[-1]
# Compare to the channel as it stood YESTERDAY ([-2]) so today's bar can break it.
upper_prev = np.asarray(upper)[-2]
lower_prev = np.asarray(lower)[-2]

print("Latest close :", round(float(close), 2))
print("20-day upper (prior bar):", round(float(upper_prev), 2))
print("20-day lower (prior bar):", round(float(lower_prev), 2))
if close > upper_prev:
    print("Signal: BREAKOUT -- close cleared the 20-day high.")
elif close < lower_prev:
    print("Signal: BREAKDOWN -- close broke the 20-day low.")
else:
    print("Signal: inside the channel -- no trade.")
```

Live output

```
Latest close : 1029.0
20-day upper (prior bar): 1251.8
20-day lower (prior bar): 1030.0
Signal: BREAKDOWN -- close broke the 20-day low.
```

As with the breakout _scan_ in Chapter 18, we compare today's close to the band as it stood on the _prior_ bar (`.shift(1)`), so today's own high can't contaminate the test. Wrapping that into a full held position and an equity-curve preview reuses the exact `flip` recipe from earlier:
EX 6A full Donchian system with curveNSEch19/06_donchian_backtest.py
Copy
```
# A full Donchian system: hold a long between breakout and breakdown, preview the curve.
import os
from datetime import datetime, timedelta

import pandas as pd
from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=400)).strftime("%Y-%m-%d")
df = client.history(symbol="LT", exchange="NSE", interval="D", start_date=start, end_date=end)

close = df["close"]
upper, _, lower = ta.donchian(df["high"], df["low"], period=20)
upper = pd.Series(upper, index=df.index)
lower = pd.Series(lower, index=df.index)

# Enter when close clears the prior upper band; exit when it loses the prior lower band.
buy = close > upper.shift(1)
sell = close < lower.shift(1)
position = pd.Series(ta.flip(buy, sell), index=df.index).astype(int)

ret = close.pct_change().fillna(0)
strat = ret * position.shift(1).fillna(0)
print("Trades opened:", int((position.diff() == 1).sum()))
print("Days held    :", int(position.sum()), "of", len(position))
print("Strategy total return: {:.1f}%".format(((1 + strat).cumprod().iloc[-1] - 1) * 100))
print("Buy & hold   total return: {:.1f}%".format(((1 + ret).cumprod().iloc[-1] - 1) * 100))
```

Live output

```
Trades opened: 4
Days held    : 160 of 273
Strategy total return: -3.8%
Buy & hold   total return: 15.8%
```

## CNC versus MIS: the product that defines the trade
Here's the detail that separates a delivery investor from a day trader, and it lives in one parameter: **product**. Every equity order carries one, and choosing wrong can wreck an otherwise good strategy.
EX 7CNC, MIS and NRML explainedNSEch19/07_cnc_vs_mis.py
Copy
```
# Delivery equity strategies use the CNC product. Here is how CNC and MIS differ.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

product_notes = {
    "CNC": "Cash & Carry -- delivery. Shares settle into your demat; hold for days, weeks or years.",
    "MIS": "Margin Intraday Square-off -- auto-closed the same session; for day trades only.",
    "NRML": "Normal -- the carry product for F&O positions held overnight.",
}

print("Equity strategy products at a glance:")
for code, note in product_notes.items():
    print(f"  {code:5s} {note}")

print("\nA golden-cross trade may hold for months, so it MUST use product='CNC'.")
print("Using 'MIS' would square off the position automatically at the close -- wrong tool.")
```

Live output

```
Equity strategy products at a glance:
  CNC   Cash & Carry -- delivery. Shares settle into your demat; hold for days, weeks or years.
  MIS   Margin Intraday Square-off -- auto-closed the same session; for day trades only.
  NRML  Normal -- the carry product for F&O positions held overnight.

A golden-cross trade may hold for months, so it MUST use product='CNC'.
Using 'MIS' would square off the position automatically at the close -- wrong tool.
```

Key idea
  * **CNC** (Cash & Carry) is for **delivery** - shares settle into your demat account and you can hold them indefinitely. Every strategy in this chapter is multi-day, so they all use `product="CNC"`.
  * **MIS** (Margin Intraday Square-off) is for **intraday only** - the broker force-closes the position at the day's end, no matter what. Use it for a golden-cross hold and your trade evaporates at 3:20 p.m. on day one.


Match the product to the holding period. Delivery strategy -> CNC. Day trade -> MIS (the focus of Chapter 20).
Finally, acting on the signal. With the server in **analyze mode** (your flight simulator from Chapter 1), placing an order is completely safe - nothing trades for real. Here we re-check the golden-cross regime and only fire a **CNC** buy if the trend is up.
EX 8Place a CNC buy on a live signalNSEch19/08_cnc_delivery_order.py
Copy
```
# Acting on a signal: place a delivery (CNC) buy. Safe to run -- server is in analyze mode.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# Re-check the regime, then only buy if the golden cross is in force.
end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=400)).strftime("%Y-%m-%d")
df = client.history(symbol="SBIN", exchange="NSE", interval="D", start_date=start, end_date=end)
close = df["close"]
bullish = ta.sma(close, 50).iloc[-1] > ta.sma(close, 200).iloc[-1]

if bullish:
    resp = client.placeorder(
        strategy="GoldenCross",
        symbol="SBIN",
        action="BUY",
        exchange="NSE",
        price_type="MARKET",
        product="CNC",   # delivery -- this is a multi-week hold
        quantity=1,
    )
    print("Regime bullish -- placed CNC buy:", resp.get("status"), resp.get("orderid"))
else:
    print("Regime not bullish -- staying flat, no order placed.")
```

Live output

```
Regime bullish -- placed CNC buy: success 26062316063085
```

Tip
This is the natural endpoint of a strategy: a rule that _checks a condition and acts only if it holds_. The `if bullish:` guard means the bot never buys into a downtrend - it simply stays flat and reports why. That discipline, encoded once, never has a bad day or a strong opinion.
## Try it yourself
  * Change the golden-cross example to use 20/100 averages instead of 50/200. More trades, more whipsaws - is the equity curve any better?
  * In the momentum ranking, shorten the lookback from 60 bars to 20. Does the leaderboard get more jumpy month to month?
  * Take the Donchian system and widen the channel from 20 to 55 days (the classic long-term setting). How does "days held" change?


## Recap
  * **Cash-equity** strategies are delivery-style: held for days to months, no leverage, settled into demat.
  * The **golden cross** (50 SMA over 200 SMA) is a textbook trend filter; the death cross is its exit.
  * An **equity-curve preview** = `flip` for the position, `.shift(1)` for honesty, `pct_change` for returns, `cumprod` to compound - always benchmarked against buy-and-hold.
  * **Momentum rotation** ranks a universe by recent return and holds the leaders - a strategy built straight from a scanner's leaderboard.
  * The **Donchian breakout** trades new N-day highs and lows; compare to the _prior_ bar's bands.
  * Choose **CNC for delivery** and MIS for intraday - the product parameter must match your holding period.


These previews are deliberately rough. Before risking real capital you need a proper, cost-aware backtest - which is exactly what we build next, first by hand and then at full power with VectorBT.
On this page
