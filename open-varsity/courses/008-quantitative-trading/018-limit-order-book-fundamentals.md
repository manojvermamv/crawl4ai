Chapters
Module C · Indian Market Microstructure - Chapter 18
# Limit Order Book Fundamentals
Bids, asks and depth - the live queue where every Indian trade is matched, read straight from real depth data.
NSEMCX
What you'll learn
  * ·Bids, asks and depth
  * ·Market vs limit orders
  * ·Reading the depth ladder
  * ·Total buy vs sell quantity
  * ·Disclosed and iceberg quantity
  * ·Reading depth() data


Until now we've talked about "the price" as if it were a single number. It isn't. The last traded price is just the most recent _handshake_ ; the **next** price is decided by a hidden queue of orders waiting to trade - the **limit order book**. This is the beating heart of every market, the place where liquidity lives and where every quant edge is ultimately born or lost. If Module C teaches you one thing, let it be how to read this book. Let's open it.
## What's really behind a price
The book has two sides: **bids** (resting buy orders, stacked below the price) and **asks** (resting sell orders, stacked above). Each line is a promise: "I'll buy 14 lots at 6819," "I'll sell 11 at 6822." Here's a live one - on an MCX crude contract, because commodities trade into the night while NSE and BSE are shut:
EX 1Read the live order bookMCXch18/01_order_book.py
Copy
```
# The order book: the live queue of who wants to buy and sell, and at what price.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# MCX commodities trade into the night, so the book is live even after NSE/BSE close.
SYMBOL, EXCHANGE = "CRUDEOIL20JUL26FUT", "MCX"
d = client.depth(symbol=SYMBOL, exchange=EXCHANGE)["data"]

print(f"{SYMBOL}   LTP {d['ltp']}\n")
print(f"{'BID qty':>9s}{'BID':>10s}   |   {'ASK':<10s}{'ASK qty':<9s}")
for bid, ask in zip(d["bids"], d["asks"]):
    print(f"{bid['quantity']:>9d}{bid['price']:>10.1f}   |   {ask['price']:<10.1f}{ask['quantity']:<9d}")

best_bid, best_ask = d["bids"][0]["price"], d["asks"][0]["price"]
print(f"\nBest bid {best_bid}  |  Best ask {best_ask}  |  Spread {best_ask - best_bid:.1f}")
print(f"Resting buy qty {d['totalbuyqty']}  vs  sell qty {d['totalsellqty']}  - a rough read on pressure")
```

Live output

```
CRUDEOIL20JUL26FUT   LTP 6820.0

  BID qty       BID   |   ASK       ASK qty  
        2    6820.0   |   6822.0    11       
       14    6819.0   |   6823.0    11       
       21    6818.0   |   6824.0    15       
       12    6817.0   |   6825.0    14       
       22    6816.0   |   6826.0    37       

Best bid 6820.0  |  Best ask 6822.0  |  Spread 2.0
Resting buy qty 71  vs  sell qty 88  - a rough read on pressure
```

Read it like a staircase meeting in the middle. The highest someone is _willing to pay_ (best bid) sits just below the lowest someone is _willing to sell at_ (best ask). Nothing trades in the gap between them; a trade only happens when someone agrees to cross it. Everything a quant cares about - liquidity, cost, short-term pressure - is visible right here, in a snapshot most traders never look at.
## Price first, then time
How does the exchange decide whose order fills when a buyer finally arrives? Two simple rules, applied in order - **price-time priority** :
Incoming market SELL 6820 (best bid) fills first Order #1 09:15:01 Order #2 09:15:02 Order #3 09:15:03 6819 fills next Order #4 Order #5 Price priority: 6820 before 6819. Time priority: within 6820, earliest order fills first. Price-time priority - the matching rule of every Indian exchange
**Price priority** : the best price always goes first - a sell hits the highest bid (6820) before touching 6819. **Time priority** : among orders at the _same_ price, the one that arrived earliest fills first - a strict first-in, first-out queue. That's the whole matching engine. It sounds trivial, but it's why being _early_ at a price matters, why HFT firms fight over microseconds (Module C, later), and why a large order eats through several levels and moves the price.
## Market orders vs limit orders
You interact with this book in two fundamentally different ways:
  * A **limit order** _joins_ the queue at a price you choose. You might get a great price - or never fill at all if the market walks away. You're a liquidity _provider_.
  * A **market order** _crosses_ the spread to trade immediately against the best resting orders. You're guaranteed a fill, but you pay for the privilege by giving up the spread. You're a liquidity _taker_.


Key idea
Every order is a trade-off between **certainty and price**. Market orders buy certainty and pay the spread; limit orders chase a better price and risk not trading at all. A quant chooses deliberately - and Module G's execution chapter is entirely about choosing well on large orders.
## The spread is a real cost
Look back at the live book: best bid 6820, best ask 6822 - a **spread** of 2. If you buy at market you pay 6822; if you immediately sell at market you receive 6820. That difference vanishes the instant you trade - it's a cost you pay before the price has moved at all. Liquid contracts have razor-thin spreads; illiquid ones can quietly cost you far more than brokerage and STT combined. We'll formalise spread, depth and impact as the true price of liquidity in the next chapter.
## Picture the book
Numbers in a table are hard to feel. Plot the same order book as a ladder and the shape of supply and demand jumps out:
EX 2The order book as a ladderMCXch18/02_depth_ladder.py
Copy
```
# Picture the order book: resting buy demand (green) vs sell supply (red) by price.
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

SYMBOL, EXCHANGE = "CRUDEOIL20JUL26FUT", "MCX"
d = client.depth(symbol=SYMBOL, exchange=EXCHANGE)["data"]

bids = pd.DataFrame(d["bids"]).assign(side="Bid (buyers)")
asks = pd.DataFrame(d["asks"]).assign(side="Ask (sellers)")
book = pd.concat([asks, bids]).sort_values("price", ascending=False)
book["level"] = book["price"].map(lambda p: f"{p:.1f}")

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(8, 4.5))
sns.barplot(data=book, x="quantity", y="level", hue="side", dodge=False,
            order=book["level"], palette={"Bid (buyers)": "#16a34a", "Ask (sellers)": "#dc2626"}, ax=ax)
ax.set_title(f"{SYMBOL} - the order book as a ladder")
ax.set_xlabel("Quantity waiting at this price")
ax.set_ylabel("Price")
ax.legend(title="")

out = Path(__file__).with_suffix(".png")
plt.savefig(out, dpi=110, bbox_inches="tight")
print(f"Best bid {d['bids'][0]['price']}  best ask {d['asks'][0]['price']}. Saved {out.name}")
```

Live output

```
Best bid 6820.0  best ask 6822.0. Saved 02_depth_ladder.png
```

![The order book as a ladder chart](https://openalgo.in/quant/charts/ch18_02_depth_ladder.png)
Green bars are resting buyers, red bars resting sellers, stacked by price. Comparing the total green against the total red - the **order-book imbalance** - gives a rough read on near-term pressure: far more resting buyers than sellers _can_ hint at support beneath the price. Treat it as one weak clue among many, never a standalone signal - it can flip in a second, and large players deliberately hide their true size.
## A note on Indian order types
The book is richer than just market and limit. On Indian exchanges you'll also meet **IOC** (immediate-or-cancel - fill what you can now, kill the rest), **SL / SL-M** (stop-loss orders that wake up only when a trigger price is hit), **GTT** (good-till-triggered, resting for days), and **disclosed / iceberg quantity** (showing only part of a big order so you don't reveal your full hand). Each is a different way of interacting with price-time priority - and a quant picks the type that leaks the least information.
## Try it yourself
  * Point the order-book example at `GOLDM03JUL26FUT` (MCX). Is gold's spread tighter or wider than crude's, relative to its price?
  * During market hours, switch to an NSE stock like `SBIN` (exchange `NSE`) and watch the book fill with real bids and asks.
  * Compute the order-book imbalance as `totalbuyqty / (totalbuyqty + totalsellqty)`. Track it over a few minutes - does it predict the next tick, or is it noise?


## Recap
  * "The price" is just the last handshake; the **limit order book** - resting **bids** below and **asks** above - decides the next one.
  * Exchanges match on **price-time priority** : best price first, then earliest order at that price (FIFO).
  * **Limit orders** join the queue (provide liquidity, risk no fill); **market orders** cross the spread (take liquidity, pay for certainty).
  * The **bid-ask spread** is a genuine, immediate cost; **order-book imbalance** is a weak pressure clue, not a signal.
  * Indian markets add **IOC, SL/SL-M, GTT and iceberg** order types - each a different way to interact with the book while leaking less information.


The book shows us _what's_ resting at each price. Next we ask the deeper question every execution desk lives on: how much will my _own_ order move the price - the economics of liquidity, spread and market impact.
On this page
