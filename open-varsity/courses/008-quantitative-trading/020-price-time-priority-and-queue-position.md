Chapters
Module C · Indian Market Microstructure - Chapter 20
# Price-Time Priority and Queue Position
How the matching engine decides who fills first, why your place in the queue is worth money, and how queue position drives passive trading.
NSENFO
What you'll learn
  * ·Price-time priority
  * ·Queue position and value
  * ·Order book events
  * ·Cancel and replace costs
  * ·Pro-rata vs FIFO matching
  * ·Queue dynamics for quants


You place a buy limit order at the best bid and it just sits there. The price ticks around it, trades print on the screen, and yet your order does not fill. Are you next in line, or are you fortieth? That single question - your **queue position** - decides whether a passive order is a clever way to earn the spread or a slow way to get run over. The last chapter showed you _what_ rests at each price. This one is about _where you stand in that pile_ , why the spot is worth real money, and how it drains.
## Price first, then time - and why time is money
Every Indian venue - NSE and BSE in equities, NFO in derivatives, MCX in commodities - matches orders on **price-time priority**. We met the rule in the order-book chapter; now look at it from inside your own order. Price comes first: the best price always trades before any worse one. Then, among all orders resting at the _same_ price, the exchange fills them in the order they arrived - a strict first-in, first-out queue.
So when you rest a buy at the best bid, you do not jump to the front. You join the _back_ of the line at that price. Everyone already there trades before you, and every new buyer who quotes your price stacks up behind you. There are exactly two ways your order climbs toward the front: an order ahead of you trades (a seller crosses and hits the bid), or an order ahead of you cancels. Your timestamp is therefore an asset. Arriving a few milliseconds earlier can be the difference between trading and not trading at all.
Key idea
Time priority means your _place in line_ , not just your price, decides whether you trade. At a given price the queue is strict FIFO - earliest order first - so being early is a genuine, and perishable, edge.
## What your spot in line is worth
Why fight for the queue at all? Because a passive fill earns the spread. A trader who crosses the spread pays it in full; you, resting at the bid, buy _at_ the bid - half a spread below the mid price. That half-spread is your reward for providing liquidity and waiting. Let us put a number on the spot using a real contract.
EX 1Your queue position and fill odds at the best bidMCXch20/01_queue_position.py
Copy
```
# Queue position at the best bid: how many lots sit ahead of you, and your fill odds.
import os
from datetime import date, timedelta

from openalgo import api
from scipy.stats import poisson

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# MCX near-month crude trades late, so its book is liveliest; fall back to a liquid NSE name.
# (symbol, exchange, lot size, tick size)
CANDIDATES = [
    ("CRUDEOIL20JUL26FUT", "MCX", 100, 1.0),
    ("RELIANCE", "NSE", 500, 0.05),
]
YOUR_LOTS = 5        # the passive BUY you want to rest at the best bid
SELL_SHARE = 0.5     # share of traded flow that arrives as sells hitting the bid
DEPTH_MINUTES = 2    # illustrative resting depth = this many minutes of real flow
HORIZON = 5          # minutes, the window for the fill-probability estimate


def recent_flow(symbol, exchange):
    end = date(2026, 6, 26)                        # last trading day (Friday)
    start = end - timedelta(days=10)
    return client.history(symbol=symbol, exchange=exchange, interval="1m",
                          start_date=start.isoformat(), end_date=end.isoformat())


for symbol, exchange, lot, tick in CANDIDATES:
    snap = client.depth(symbol=symbol, exchange=exchange).get("data", {})
    df = recent_flow(symbol, exchange)
    if df is None or len(df) == 0:
        continue
    flow = float(df["volume"].median())            # real lots traded per minute
    bids, asks = snap.get("bids", []), snap.get("asks", [])
    live = bool(bids) and bids[0].get("quantity", 0) > 0

    if live:                                        # market open: read the real touch
        best_bid = float(bids[0]["price"])
        ahead = float(bids[0]["quantity"])
        spread = float(asks[0]["price"]) - best_bid
        mode = "live book"
    else:                                           # off-hours: rebuild around the real last price
        ltp = float(snap.get("ltp") or df["close"].iloc[-1])
        best_bid = round(ltp / tick) * tick - tick
        spread = tick                               # a liquid contract trades about one tick wide
        ahead = round(DEPTH_MINUTES * flow)         # illustrative resting depth from real flow
        mode = "reconstructed (book closed; depth seeded from real 1m flow)"

    sell_rate = flow * SELL_SHARE                   # lots/min hitting the bid
    wait_front = ahead / sell_rate                  # time for the queue ahead to clear
    wait_full = (ahead + YOUR_LOTS) / sell_rate     # time to also fill your lots
    mu = sell_rate * HORIZON                         # expected sells over the horizon
    p_full = float(poisson.sf(ahead + YOUR_LOTS - 1, mu))   # P(N >= ahead + your lots)
    queue_value = (spread / 2.0) * lot              # half-spread earned per lot vs the mid

    print(f"{symbol}  [{mode}]")
    print(f"  best bid {best_bid:g}   spread {spread:g}   tick {tick:g}   lot {lot}")
    print(f"  resting ahead of you at the best bid : {ahead:.0f} lots")
    print(f"  your passive BUY joins the back      : {YOUR_LOTS} lots")
    print(f"  sell flow hitting the bid (real)     : {sell_rate:.1f} lots/min "
          f"(median {flow:.0f} lots/min traded)")
    print(f"  expected wait to reach the front     : {wait_front:.1f} min")
    print(f"  expected wait to fully fill          : {wait_full:.1f} min")
    print(f"  P(full fill within {HORIZON} min)            : {p_full * 100:.0f}%")
    print(f"  a good queue spot is worth           : Rs {queue_value:.0f}/lot "
          f"(Rs {queue_value * YOUR_LOTS:.0f} on {YOUR_LOTS} lots)")
    print(f"SUMMARY {symbol}: {ahead:.0f} lots ahead, ~{wait_front:.1f} min to the front, "
          f"~{p_full * 100:.0f}% full fill in {HORIZON} min, queue spot worth Rs {queue_value:.0f}/lot.")
    break
```

Live output

```
CRUDEOIL20JUL26FUT  [reconstructed (book closed; depth seeded from real 1m flow)]
  best bid 6569   spread 1   tick 1   lot 100
  resting ahead of you at the best bid : 60 lots
  your passive BUY joins the back      : 5 lots
  sell flow hitting the bid (real)     : 15.0 lots/min (median 30 lots/min traded)
  expected wait to reach the front     : 4.0 min
  expected wait to fully fill          : 4.3 min
  P(full fill within 5 min)            : 89%
  a good queue spot is worth           : Rs 50/lot (Rs 250 on 5 lots)
SUMMARY CRUDEOIL20JUL26FUT: 60 lots ahead, ~4.0 min to the front, ~89% full fill in 5 min, queue spot worth Rs 50/lot.
```

Because the book is shut over the weekend, the script reconstructs an illustrative ladder around the real last price and seeds it from genuine flow - it says so plainly. On the near-month crude future the best bid sits at 6569 with a one-tick spread, and the median traded flow on the last session was 30 lots a minute. We assume 60 lots already rest ahead of you and you join the back with 5 lots. With about half the flow arriving as sells that hit the bid - 15 lots a minute - you would expect roughly 4.0 minutes to reach the front, and a Poisson arrival model puts the chance of a _full_ fill within 5 minutes at about 89%. The spot itself is worth Rs 50 per lot - half of the one-rupee spread across the 100-barrel lot - or Rs 250 on your 5 lots. Tiny per clip, but a market maker earns it thousands of times a day.
Heads up
The queue spot is not free money. You tend to fill exactly when you would rather not - a seller lifts your bid an instant before the price drops, so you buy just before it falls. The half-spread you earn is partly compensation for this **adverse selection**. A plan that says "I will simply earn the spread" and ignores it will quietly bleed.
Incoming market SELL Best bid 6569 Order #1 fills first Order #2 then Order #3 then ... ... YOUR 5 lots at the back, fills last about 60 lots ahead of you - all of them fill before a single one of yours does Price-time priority: same price, earliest order first. Time in the queue is a real, tradeable asset. Queue position at the best bid - your order rests behind everyone who arrived earlier
## How the queue actually drains
Three kinds of **order-book events** change a queue: a new order _adds_ to it, a _cancel_ removes one, and a _trade_ fills from the front. Your position is the running tally of everything still ahead of you. Let us simulate that tally falling, with the event rates anchored to real flow.
EX 2A FIFO queue draining in real timeMCXch20/02_queue_drain.py
Copy
```
# Watch a FIFO bid queue drain: your position falls as sells fill and orders ahead cancel.
import os
from datetime import date, timedelta
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

SYMBOL, EXCHANGE = "CRUDEOIL20JUL26FUT", "MCX"
YOUR_LOTS = 5         # your passive BUY, resting at the back of the best-bid queue
SELL_SHARE = 0.5      # share of flow that arrives as sells hitting the bid
CANCEL_MULT = 1.2     # cancels-ahead per sell (real books cancel more than they trade)
DEPTH_MINUTES = 2     # illustrative depth ahead of you = this many minutes of real flow

# Real per-minute flow from the last trading day drives the event rates.
end = date(2026, 6, 26)
start = end - timedelta(days=10)
df = client.history(symbol=SYMBOL, exchange=EXCHANGE, interval="1m",
                    start_date=start.isoformat(), end_date=end.isoformat())
flow = float(df["volume"].median())               # real lots/min

rng = np.random.default_rng(7)
ahead0 = round(DEPTH_MINUTES * flow)              # lots in front of you when you join
sell_ps = flow * SELL_SHARE / 60.0               # sells per second hitting the bid
cancel_ps = sell_ps * CANCEL_MULT                # cancels-ahead per second (scaled by queue left)

t, ahead, yours = 0, ahead0, YOUR_LOTS
times, ahead_path = [0], [ahead0]
front_t = fill_t = None
while yours > 0 and t < 1800:                     # cap the sim at 30 minutes
    t += 1
    cancels = rng.poisson(cancel_ps * (ahead / ahead0)) if ahead > 0 else 0
    ahead = max(0, ahead - cancels)              # cancels ahead advance you but never fill you
    sells = rng.poisson(sell_ps)
    eat = min(ahead, sells)                       # sells first clear the queue ahead...
    ahead -= eat
    sells -= eat
    if ahead == 0 and front_t is None:
        front_t = t
    if ahead == 0 and sells > 0:                  # ...then fill your lots, FIFO
        yours = max(0, yours - sells)
        if yours == 0 and fill_t is None:
            fill_t = t
    times.append(t)
    ahead_path.append(ahead)

mins = np.array(times) / 60.0
sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(mins, ahead_path, color="#7c83ff", linewidth=2, label="lots ahead of you")
ax.axhline(0, color="#9a9a9a", linewidth=1)
if front_t:
    ax.axvline(front_t / 60.0, color="#16a34a", linestyle="--", linewidth=1.4,
               label=f"reached front ({front_t / 60.0:.1f} min)")
if fill_t:
    ax.axvline(fill_t / 60.0, color="#dc2626", linestyle="--", linewidth=1.4,
               label=f"fully filled ({fill_t / 60.0:.1f} min)")
ax.set_title(f"{SYMBOL} - your position in the FIFO bid queue draining")
ax.set_xlabel("Minutes after you joined the back of the queue")
ax.set_ylabel("Lots resting ahead of you")
ax.legend(loc="upper right")

out = Path(__file__).with_suffix(".png")
plt.savefig(out, dpi=110, bbox_inches="tight")

filled = "did not fully fill" if fill_t is None else f"fully filled in {fill_t / 60.0:.1f} min"
print(f"SUMMARY {SYMBOL}: joined behind {ahead0} lots, reached the front in "
      f"{(front_t or 0) / 60.0:.1f} min and {filled} (real flow {flow:.0f} lots/min). Saved {out.name}")
```

Live output

```
SUMMARY CRUDEOIL20JUL26FUT: joined behind 60 lots, reached the front in 2.4 min and fully filled in 2.8 min (real flow 30 lots/min). Saved 02_queue_drain.png
```

![A FIFO queue draining in real time chart](https://openalgo.in/quant/charts/ch20_02_queue_drain.png)
Starting 60 lots back, and driven by the same real 30-lots-a-minute crude flow plus a realistic dose of cancellations, the simulation reached the front in **2.4 minutes** and fully filled your 5 lots by **2.8 minutes**. Notice the gap from the first example: there the naive estimate from trades alone was 4.0 minutes to the front, yet the simulation got there in 2.4. The reason is the second event type - _cancels ahead of you advance your position for free_. You inherit a vacated spot without a single trade printing. Real books cancel far more than they trade (we quantify the order-to-trade ratio in the HFT module, ch35), so the effective queue is shorter than the visible depth suggests. That cuts both ways: the same churn that pulls you forward can also make the liquidity you were counting on vanish before it ever trades.
Tip
Model the queue, do not eyeball the depth. The size showing at the bid overstates how long you will wait, because much of it cancels before it trades. Track trade flow and cancel flow separately - the cancel rate is often the bigger driver of how fast you reach the front.
## Cancel and replace: forfeiting your place
Here is the trap that catches passive quants. Your time priority is bound to your order's identity. If you **cancel and replace** to chase the price, or to _increase_ your quantity, the exchange treats it as a brand-new order: you drop to the _back_ of the queue and forfeit every second of priority you had banked. Reducing quantity usually keeps your spot, but raising it or repricing does not. So every casual "let me just nudge my quote" throws away the queue position you had already paid for in patience.
For anyone quoting at speed this **cancel/replace cost** is a genuine expense, not a rounding error. A spot near the front of a liquid queue is an asset worth real basis points, and you destroy it the moment you reprice. The whole craft of passive quoting is to choose a price you can _leave alone_ , so you rarely have to surrender your place.
Note
On NSE a price modification or a quantity increase loses time priority and sends your order to the back of the queue; a quantity decrease typically retains it. Before you cancel-replace, ask whether the better price is worth surrendering the place in line you already hold.
## FIFO versus pro-rata
One last rule changes everything about how you size a passive quote: how the exchange splits a trade among orders at the same price. India uses **price-time priority** - strict FIFO, the model behind every number above. Some venues, and certain deeply liquid products elsewhere such as some interest-rate futures, instead use **pro-rata** matching, where an incoming trade is allocated in proportion to each resting order's _size_ rather than its arrival time.
The strategic consequences are opposite. Under FIFO you race for time, and a small order at the front beats a huge one behind it - speed and patience win. Under pro-rata, arrival time barely matters, so participants quote _much larger_ than they truly want, knowing they will only ever get a slice. That inflates the displayed depth and rewards size over speed. Know which regime you are trading before you design a passive strategy. For India it is FIFO, so your edge is to be early and to reprice as little as possible.
## Queue dynamics for the passive quant
Put it together. A resting limit order is a position in a hidden queue, and that position has a value - the half-spread you stand to earn, Rs 50 a lot on our crude example - and a cost - the adverse selection you absorb and the priority you forfeit each time you reprice. The passive quant's whole job is to win the queue and keep it: quote early, quote where you can leave it, cancel sparingly, and size for FIFO. The numbers say a good spot in a liquid book is worth a few hundred rupees a clip and fills in a couple of minutes - trivial per trade, decisive at scale.
Next we turn from the order that _waits_ to the order that _cannot_ - the large trade that must cross the spread, walk the book, and pay to move the price. That is the economics of liquidity and impact cost.
On this page
