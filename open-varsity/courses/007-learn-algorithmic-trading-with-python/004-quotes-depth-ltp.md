Chapters
Module A · Foundations - Chapter 04
# Quotes, Depth & LTP
Pull live snapshots - single quotes, batched multiquotes and full order-book depth.
NSENFOMCX
What you'll learn
  * ·quotes() for one symbol
  * ·multiquotes() for many
  * ·depth() order book
  * ·Bid/ask spread
  * ·Quotes across exchanges
  * ·Building a quote board


Before you can act on the market, you have to _see_ it clearly. In Chapter 1 you pulled your first price; now let's open the whole toolbox. OpenAlgo gives you three different windows into live prices, and each answers a different question:
  * A **quote** - a rich snapshot of one instrument. _"How is Reliance doing right now?"_
  * **Multiquotes** - many instruments in a single fast request. _"How's my whole watchlist?"_
  * **Depth** - the order book itself, the live queue of buyers and sellers. _"Who's waiting to trade, and at what price?"_


We'll work through all three, across NSE, NFO and MCX. By the end you'll have a reusable quote board you can drop into a dashboard later.
## A single quote, in full
`client.quotes()` returns a **dictionary** (those `key: value` boxes from Chapter 2) describing one symbol. Rather than guess what's inside, let's print every field so you know exactly what you're working with.
EX 1Every field in a quoteNSEch04/01_single_quote.py
Copy
```
# A full quote snapshot: every field the server returns for one symbol.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

q = client.quotes(symbol="SBIN", exchange="NSE")["data"]
for field, value in q.items():
    print(f"{field:12s}: {value}")
```

Live output

```
ask         : 1024.2
bid         : 0
high        : 1045.5
low         : 1022.35
ltp         : 1024.2
oi          : 0
open        : 1041
prev_close  : 1040.75
volume      : 10411004
```

Let's translate that jargon into plain trading terms:
  * **ltp** - _Last Traded Price_ , the most recent price a trade happened at. This is "the price" most of the time.
  * **open / high / low** - where the day started, and its highest and lowest points so far.
  * **prev_close** - yesterday's closing price, the baseline you measure today's move against.
  * **volume** - how many shares/contracts have changed hands today (a gauge of activity).
  * **oi** - _Open Interest_ , only for derivatives - how many contracts are currently live.


Now let's pull a few of those and compute the day's change, the way you'd glance at a stock each morning.
EX 2Useful numbers from a quoteNSEch04/02_quote_fields.py
Copy
```
# Pick the fields you need and turn them into useful numbers.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

q = client.quotes(symbol="RELIANCE", exchange="NSE")["data"]
change = q["ltp"] - q["prev_close"]

print("LTP        :", q["ltp"])
print("Day range  :", q["low"], "to", q["high"])
print("Prev close :", q["prev_close"])
print("Volume     :", q["volume"])
print("Change     :", round(change, 2), f"({change / q['prev_close'] * 100:.2f}%)")
```

Live output

```
LTP        : 1309.5
Day range  : 1304 to 1333
Prev close : 1326.5
Volume     : 15400184
Change     : -17.0 (-1.28%)
```

## Many symbols at once
You _could_ call `quotes()` inside a loop, but that fires one network request per symbol - slow for a 50-stock watchlist. `client.multiquotes()` fetches the whole list in a **single** request. You hand it a list of `{"symbol", "exchange"}` dictionaries and get back a `results` list to loop over.
EX 3Batch quotes for a watchlistNSEch04/03_multiquotes.py
Copy
```
# multiquotes() fetches many symbols in a single request -- far faster than a loop.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

symbols = [{"symbol": s, "exchange": "NSE"} for s in ["RELIANCE", "TCS", "INFY", "HDFCBANK"]]
results = client.multiquotes(symbols=symbols)["results"]

for r in results:
    print(f"{r['symbol']:10s} {r['data']['ltp']:>10.2f}")
```

Live output

```
RELIANCE      1309.50
TCS           2059.60
INFY          1029.30
HDFCBANK       774.65
```

The real beauty: that list can mix exchanges freely. One call can return a stock, an index future, and a commodity together.
EX 4One call, three exchangesNSENFOMCXch04/04_multiquotes_exchanges.py
Copy
```
# One multiquotes call can span NSE, NFO and MCX together.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

symbols = [
    {"symbol": "RELIANCE", "exchange": "NSE"},
    {"symbol": "NIFTY30JUN26FUT", "exchange": "NFO"},
    {"symbol": "GOLDM03JUL26FUT", "exchange": "MCX"},
]
for r in client.multiquotes(symbols=symbols)["results"]:
    print(f"{r['exchange']:4s} {r['symbol']:18s} {r['data']['ltp']:>12.2f}")
```

Live output

```
NSE  RELIANCE                1309.50
NFO  NIFTY30JUN26FUT        23810.00
MCX  GOLDM03JUL26FUT       144335.00
```

Tip
Reach for `multiquotes()` whenever you need more than two or three symbols. Fewer requests means faster responses and less strain on your broker connection - which really matters in a live scanner refreshing every few seconds.
## The order book: depth
A quote tells you the _last_ price. **Depth** (the order book) shows you the _next_ prices - the stacked queue of buy orders (called **bids**) sitting just below, and sell orders (**asks**) sitting just above. `client.depth()` returns up to five levels on each side, plus the total quantity waiting to buy and to sell.
Note
Depth is a _live_ view, so it only means anything while a market is open. NSE and BSE trade 09:15-15:30 IST; **MCX commodities trade much later, into the evening.** The examples here use an MCX contract so you can see a real, moving order book even after stock hours - just swap in an NSE symbol during the trading day.
EX 5Read the order bookMCXch04/05_depth.py
Copy
```
# depth() returns the order book: the best buy (bid) and sell (ask) levels.
# We use an MCX commodity here so the book is live in the evening session.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

d = client.depth(symbol="CRUDEOIL20JUL26FUT", exchange="MCX")["data"]
print("LTP:", d["ltp"], "| total buy:", d["totalbuyqty"], "| total sell:", d["totalsellqty"])
print("Bids (buyers)        Asks (sellers)")
for bid, ask in zip(d["bids"][:5], d["asks"][:5]):
    print(f"  {bid['price']:>9.2f} x {bid['quantity']:<6}  {ask['price']:>9.2f} x {ask['quantity']}")
```

Live output

```
LTP: 7011 | total buy: 57 | total sell: 57
Bids (buyers)        Asks (sellers)
    7007.00 x 5         7009.00 x 4
    7006.00 x 12        7010.00 x 10
    7005.00 x 13        7011.00 x 15
    7004.00 x 10        7012.00 x 13
    7003.00 x 17        7013.00 x 15
```

Read that book like this: the highest someone is _willing to pay_ (best bid) sits just under the lowest someone is _willing to sell at_ (best ask). Trades happen where they meet.
## The bid-ask spread
The gap between the best bid and the best ask is the **spread** - and it's a hidden cost you pay on every trade. If you buy "at market", you pay the ask; if you sell at market, you receive the bid. That difference is gone the instant you trade. Liquid contracts have razor-thin spreads; thinly traded ones can quietly cost you far more than brokerage.
EX 6Measure the spreadMCXch04/06_spread.py
Copy
```
# The bid-ask spread is your hidden cost on every trade. Tighter is cheaper.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

d = client.depth(symbol="GOLDM03JUL26FUT", exchange="MCX")["data"]
best_bid = d["bids"][0]["price"] if d["bids"] else 0
best_ask = d["asks"][0]["price"] if d["asks"] else 0
print("Best bid:", best_bid, "| best ask:", best_ask)

if best_bid and best_ask:
    spread = best_ask - best_bid
    print("Spread  :", round(spread, 2), f"({spread / best_ask * 100:.3f}%)")
else:
    print("Market is closed -- no live bids/asks right now.")
```

Live output

```
Best bid: 144335 | best ask: 144357
Spread  : 22 (0.015%)
```

Heads up
A wide spread is a red flag. On an illiquid option or a low-volume stock, the spread can be several percent - meaning you start every trade deep in the red before the price moves at all. Always check the spread before trading something unfamiliar.
## Order-book imbalance
Comparing the total buy quantity against the total sell quantity gives a rough read on short-term pressure: many more resting buyers than sellers _can_ hint at support underneath the price. Treat it as one weak clue among many - never a standalone reason to trade.
EX 7Buy vs sell pressureMCXch04/07_depth_imbalance.py
Copy
```
# Total buy vs sell quantity hints at short-term pressure in the book.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

d = client.depth(symbol="CRUDEOIL20JUL26FUT", exchange="MCX")["data"]
buy_qty, sell_qty = d["totalbuyqty"], d["totalsellqty"]
total = buy_qty + sell_qty

print("Total buy qty :", buy_qty)
print("Total sell qty:", sell_qty)
if total:
    print("Buy pressure  :", f"{buy_qty / total * 100:.1f}%")
```

Live output

```
Total buy qty : 60
Total sell qty: 51
Buy pressure  : 54.1%
```

## Build a quote board
Let's combine what we've learned into a small, reusable **function** - a multi-exchange quote board that prints each symbol's price and daily change in a neat table. This is exactly the component we'll wire into a live Streamlit dashboard in Chapter 10, so it's worth understanding now.
EX 8A reusable quote boardNSENFOMCXch04/08_quote_board.py
Copy
```
# A reusable quote board across exchanges -- the heart of any dashboard.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)


def quote_board(items):
    print(f"{'EXCH':5s}{'SYMBOL':20s}{'LTP':>12s}{'CHG%':>9s}")
    for r in client.multiquotes(symbols=items)["results"]:
        d = r["data"]
        pct = (d["ltp"] - d["prev_close"]) / d["prev_close"] * 100 if d["prev_close"] else 0
        print(f"{r['exchange']:5s}{r['symbol']:20s}{d['ltp']:>12.2f}{pct:>8.2f}%")


quote_board([
    {"symbol": "RELIANCE", "exchange": "NSE"},
    {"symbol": "NIFTY30JUN26FUT", "exchange": "NFO"},
    {"symbol": "CRUDEOIL20JUL26FUT", "exchange": "MCX"},
])
```

Live output

```
EXCH SYMBOL                       LTP     CHG%
NSE  RELIANCE                 1309.50   -1.28%
NFO  NIFTY30JUN26FUT         23810.00   -1.30%
MCX  CRUDEOIL20JUL26FUT       7011.00    0.40%
```

## Open interest on derivatives
Futures and options quotes carry an extra number stocks don't: **open interest (OI)** - the count of contracts currently outstanding. Read alongside price it's a useful tell: rising price _with_ rising OI suggests fresh money pushing the move, while rising price with _falling_ OI can mean short-covering that may fizzle. We'll use it properly in the F&O chapters.
EX 9Open interest on a futureNFOch04/09_futures_oi.py
Copy
```
# Futures and options quotes also carry open interest (OI) -- live contracts outstanding.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

q = client.quotes(symbol="NIFTY30JUN26FUT", exchange="NFO")["data"]
print("NIFTY future LTP :", q["ltp"])
print("Open interest    :", q["oi"])
print("Volume           :", q["volume"])
```

Live output

```
NIFTY future LTP : 23810
Open interest    : 16290430
Volume           : 3711825
```

## Where in the day's range?
One last quick read. Knowing whether price is hugging the day's high or sitting near the low tells you something about intraday strength at a glance - bulls in control near the highs, bears near the lows.
EX 10Position within the day rangeNSEch04/10_range_position.py
Copy
```
# Where is price sitting inside today's range? A quick read on intraday strength.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

q = client.quotes(symbol="TCS", exchange="NSE")["data"]
day_range = q["high"] - q["low"]
position = (q["ltp"] - q["low"]) / day_range * 100 if day_range else 0

print(f"Low {q['low']}   LTP {q['ltp']}   High {q['high']}")
print(f"Trading at {position:.0f}% of today's range")
```

Live output

```
Low 2055   LTP 2059.6   High 2114
Trading at 8% of today's range
```

## Try it yourself
  * Replace the watchlist in the multiquotes example with five stocks you actually follow.
  * During market hours, point the depth example at an NSE stock like `SBIN` and watch the book fill with real bids and asks.
  * Add `INDIAVIX` (exchange `NSE_INDEX`) to the quote board and see the volatility index alongside your prices.


## Recap
  * `quotes()` returns a rich snapshot of one symbol - reach for `ltp`, `open/high/low`, `prev_close`, `volume`, and `oi`.
  * `multiquotes()` fetches many symbols, even across exchanges, in **one** fast request - prefer it for watchlists and scanners.
  * `depth()` exposes the live order book: bids, asks, and total quantities. It's empty when the market is shut, so use MCX for evening practice.
  * The **spread** is a genuine trading cost; **imbalance** and **open interest** are supporting clues, not triggers.
  * A `multiquotes`-powered quote board is a building block we'll reuse in dashboards and scanners.


So far we've only looked at the _present_. The real analytical power comes from the _past_ - and that's next: downloading historical OHLCV candles at any timeframe and reshaping them for study.
On this page
