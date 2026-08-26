Chapters
Module 5 · Python for the Markets - Chapter 38
# Live Quotes & Delayed Data
The difference between a live price and yesterday's close - pull live Indian quotes from OpenAlgo and delayed US data from yfinance, side by side.
NSELIVEUS
What you'll learn
  * ·Live vs delayed data
  * ·Live LTP from OpenAlgo
  * ·US quotes from yfinance
  * ·Why the gap matters
  * ·Quote fields explained
  * ·Building a quote board


You've now pulled data two ways: delayed, from yfinance, and live, from OpenAlgo. They look similar in code, but the difference between them is the difference between _studying_ the market and _trading_ it. This chapter puts them side by side, decodes every field in a quote, and builds a small live quote board - the kind of thing you'd glance at all day.
## A live quote board
A "quote" is the current snapshot of a stock. With OpenAlgo you can pull several at once and lay them out as a board, using the f-string alignment from Chapter 7:
EX 1A live quote board, straight from the marketPYch38/01_quote_board.py
Copy
```
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

symbols = ["RELIANCE", "TCS", "INFY", "SBIN"]

# A live quote board - one row per symbol, aligned with the f-string tricks from Chapter 7.
print(f"{'Symbol':<12}{'LTP':>12}{'Prev close':>14}")
print("-" * 38)
for s in symbols:
    data = client.quotes(symbol=s, exchange="NSE")["data"]
    print(f"{s:<12}{data['ltp']:>12,.2f}{data['prev_close']:>14,.2f}")
```

Live output

```
Symbol               LTP    Prev close
--------------------------------------
RELIANCE        1,313.60      1,313.60
TCS             2,109.00      2,109.00
INFY            1,056.60      1,056.60
SBIN            1,034.60      1,034.60
```

Four live LTPs - last traded prices - in a clean, aligned table. This is the heartbeat of any trading screen: a loop over your watchlist, one quote each, refreshed as often as you like. (Here `prev_close` equals `ltp` because the sandbox is quiet; on a live feed during market hours they differ, giving you the day's change.)
## What's in a quote?
A quote is more than one number. Pull the full record and you get the whole picture of supply and demand:
EX 2Every field in a quote, explainedPYch38/02_quote_fields.py
Copy
```
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

q = client.quotes(symbol="RELIANCE", exchange="NSE")["data"]

print("RELIANCE - a full quote:")
for field in ["ltp", "prev_close", "open", "high", "low", "bid", "ask", "volume"]:
    print(f"  {field:<11}: {q.get(field)}")
```

Live output

```
RELIANCE - a full quote:
  ltp        : 1313.6
  prev_close : 1313.6
  open       : 0.0
  high       : 0.0
  low        : 0.0
  bid        : 0.0
  ask        : 0.0
  volume     : 0
```

Here's what each field means:
  * **`ltp`**-**last traded price** , the single most-watched number.
  * **`prev_close`**- yesterday's closing price;`ltp - prev_close` is the day's change.
  * **`open`/`high` / `low`** - today's first price and its range so far.
  * **`bid`/`ask`** - the best price someone will _buy_ at (`bid`) and _sell_ at (`ask`); the gap between them is the **spread**.
  * **`volume`**- shares traded today, a gauge of activity.


Note
In our analyze-mode sandbox, `open`, `high`, `low`, `bid`, `ask` and `volume` read **0** - it streams the last price but not the full intraday book. With a live broker feed during market hours, every field carries a real number. The point here is the _shape_ of a quote and what each field means, so you recognise them anywhere.
Key idea
A **quote** is a snapshot: **`ltp`**(last price),**`prev_close`**(for the day's change),**`open`/`high` /`low`**, **`bid`/`ask`** (best buy/sell, whose gap is the **spread**), and **`volume`**. The**LTP** is the headline; the rest fills in the context.
## Live versus delayed
Free feeds like yfinance are **delayed** - typically by about 15 minutes - while a broker feed like OpenAlgo is **live**. Put them head to head:
EX 3Live (OpenAlgo) versus delayed (yfinance)PYch38/03_live_vs_delayed.py
Copy
```
import os

import yfinance as yf
from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# Live: straight from the broker feed via OpenAlgo.
live = client.quotes(symbol="RELIANCE", exchange="NSE")["data"]["ltp"]

# Delayed: a free feed (yfinance) - good for study, but it lags the real market.
delayed = float(yf.Ticker("RELIANCE.NS").history(period="2d")["Close"].dropna().iloc[-1])

print(f"OpenAlgo (live)    : {live:>10.2f}")
print(f"yfinance (delayed) : {delayed:>10.2f}")
print(f"Difference         : {live - delayed:>+10.2f}")
```

Live output

```
OpenAlgo (live)    :    1313.60
yfinance (delayed) :    1313.60
Difference         :      +0.00
```

Right now the difference is **zero** - and that's instructive, not a bug. When the market is quiet or closed, the delayed feed has caught up to the same settled price, so the two agree. The gap only opens when price is _moving_ :
1,309 1,314 delayed feed (~15 min ago) live feed (now) Illustrative: a delayed feed shows where price *was*; the live feed shows where it *is*. The faster the market, the wider the gap.
In a fast-moving market those 15 minutes can be several percent - which is exactly why you study history on free delayed data, but place real orders on a live feed.
Did you know?
**For the fastest traders, the speed of light is a real constraint.** A few seconds of delay is nothing to us, but high-frequency firms fight over _microseconds_. They pay handsomely to place their servers in the very same building as the exchange's matching engine - a practice called **colocation** - because light travels only about 30 centimetres in a nanosecond, so even the length of a network cable becomes a competitive edge. At the bleeding edge of trading, physics itself sets the speed limit.
## When do you actually need live?
The honest answer for a learner: **not yet**. Studying history, testing ideas, building the skills in this course - all of it is fine on free, delayed data. You only _need_ a live feed when you're placing real orders and the exact current price matters. So learn on delayed data without guilt; reach for live (OpenAlgo) when you graduate to real execution.
## Try it yourself
  * Add `HDFCBANK` and `ICICIBANK` to the quote board and re-run it.
  * Compute the day's change in the board: print `ltp - prev_close` as an extra right-aligned column.
  * Run the live-vs-delayed comparison a few times during active market hours and watch whether the difference grows.


## Recap
  * A **quote** is a snapshot: **`ltp`**is the headline;**`prev_close`**,**`open`/`high` /`low`**, **`bid`/`ask`** (the **spread**) and **`volume`**fill in the picture.
  * Build a **quote board** by looping your watchlist and printing an aligned table.
  * **Delayed** feeds (yfinance, ~15 min) are perfect for study; **live** feeds (OpenAlgo) matter when you actually trade - the gap widens as the market moves.
  * You only truly need live data when **placing real orders**.


There's one more way market data reaches you - and it's the opposite of everything in the last two chapters. Instead of _asking_ for a quote each time, you can have prices **streamed** to you the instant they change. That's a **WebSocket** , and the next chapter explains the idea in plain words.
On this page
