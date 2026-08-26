Chapters
Module C · Indian Market Microstructure - Chapter 19
# Order Types and the Order Lifecycle
Every order type on Indian exchanges and the full life of an order - entry, modification, cancellation, the audit trail and client-code controls.
NSE
What you'll learn
  * ·Market, limit, SL and SL-M
  * ·IOC, GTT and iceberg
  * ·Order entry and modification
  * ·Cancellation and the audit trail
  * ·UCC and client-code controls
  * ·Product types (MIS, NRML, CNC)


In the last chapter we learned to _read_ the book. Now we learn to _talk_ to it. Every interaction you have with the market - every entry, every exit, every stop - is an **order** , and an order is not a single instant. It is born, it lives, and it dies, passing through a small set of states with a precise timestamp on each transition. Quants who bleed money on execution almost never lose it on the idea. They lose it here, in the gap between "I want to buy" and "I am filled". So let us be deliberate about exactly what we are sending, and exactly what happens to it after we hit send.
## The menu of order types
An order is an instruction with a _type_ , and the type decides how it meets price-time priority. On Indian exchanges you have a compact but expressive menu.
  * A **market order** crosses the spread and fills now at the best available price. Certainty of fill, no certainty of price.
  * A **limit order** rests in the book at a price you choose and fills only at that price or better. Certainty of price, no certainty of fill.
  * A **stop-loss limit (SL)** order is dormant until the market touches a **trigger price** ; it then becomes a limit order at a price you set. It protects a position or arms a breakout.
  * A **stop-loss market (SL-M)** order is the same, except on trigger it becomes a _market_ order - guaranteed to fire, at whatever price the book offers.
  * **IOC** (immediate-or-cancel) fills whatever it can the instant it arrives and kills the unfilled remainder. No resting, no information leak.
  * **GTT** (good-till-triggered) is a broker-side resting instruction that watches the market for days and submits an order only when your condition trips.
  * **Iceberg / disclosed quantity** shows the book only a slice of a large order at a time, so you do not reveal your full hand to faster participants.


Key idea
Every order type is a different answer to one question: how do I trade off **certainty of fill** against **certainty of price** , while leaking as little information as possible? Pick the type that matches your intent, not the one your hand defaults to.
The cleanest way to feel the difference is to price a single real trade four ways. The example below pulls the live last-traded price for a liquid name and lays out what each order type would actually do around it - no order is placed, this is pure construction from the quote.
EX 1One trade, priced four ways from a live quoteNSEch19/01_order_types_table.py
Copy
```
# What each order type would do for a long trade, built from a real live LTP.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

SYMBOL, EXCHANGE, TICK = "RELIANCE", "NSE", 0.05
ltp = client.quotes(symbol=SYMBOL, exchange=EXCHANGE)["data"]["ltp"]


def to_tick(p):  # snap a price to the exchange tick size
    return round(round(p / TICK) * TICK, 2)


# A long-trade plan framed around the live last-traded price. No order is placed.
limit_entry = to_tick(ltp * 0.997)        # patient buy, a touch below the market
stop_trig = to_tick(ltp * 0.99)           # protective stop trigger, 1% below
stop_limit = to_tick(stop_trig - 0.5)     # SL limit price, just below the trigger
target = to_tick(ltp * 1.02)              # profit target, 2% above

print(f"{SYMBOL}  {EXCHANGE}   LTP {ltp:.2f}   (tick {TICK})\n")
print(f"{'Order type':<14}{'Side':<6}{'Trigger':>10}{'Price':>10}   Behaviour")
rows = [
    ("MARKET", "BUY", None, ltp, "fills now at best available, pays the spread"),
    ("LIMIT", "BUY", None, limit_entry, "rests in book, fills only at <= limit"),
    ("SL", "SELL", stop_trig, stop_limit, "protective stop, wakes at trigger then limit"),
    ("SL-M", "SELL", stop_trig, None, "protective stop, wakes at trigger then market"),
    ("TARGET (LIMIT)", "SELL", None, target, "books profit, fills only at >= price"),
]
for name, side, trig, price, note in rows:
    t = f"{trig:.2f}" if trig is not None else "-"
    p = f"{price:.2f}" if price is not None else "market"
    print(f"{name:<14}{side:<6}{t:>10}{p:>10}   {note}")

risk = round(limit_entry - stop_limit, 2)
reward = round(target - limit_entry, 2)
print(f"\nLimit entry {limit_entry:.2f}: risk/share {risk:.2f}, reward/share {reward:.2f}, "
      f"reward-to-risk {reward / risk:.2f} to 1")
```

Live output

```
RELIANCE  NSE   LTP 1318.10   (tick 0.05)

Order type    Side     Trigger     Price   Behaviour
MARKET        BUY            -   1318.10   fills now at best available, pays the spread
LIMIT         BUY            -   1314.15   rests in book, fills only at <= limit
SL            SELL     1304.90   1304.40   protective stop, wakes at trigger then limit
SL-M          SELL     1304.90    market   protective stop, wakes at trigger then market
TARGET (LIMIT)SELL           -   1344.45   books profit, fills only at >= price

Limit entry 1314.15: risk/share 9.75, reward/share 30.30, reward-to-risk 3.11 to 1
```

When this ran, the last-traded price was 1318.10. A patient **limit** buy sits at 1314.15, a touch below the market, hoping the price comes to you. A protective **SL** to exit a long arms at a trigger of 1304.90 and then works a limit at 1304.40; the **SL-M** twin arms at the same 1304.90 but converts to a market order so it cannot be left stranded. The **target** is a limit sell at 1344.45. Framed this way the trade has a risk of 9.75 per share against a reward of 30.30, a reward-to-risk of 3.11 to 1 - geometry you can see _before_ you commit a single rupee.
Heads up
An SL-M order will fire on trigger but gives you no control over the fill price; in a fast or gapping market it can fill far past your trigger. An SL limit protects the price but can be skipped entirely if the market jumps through your limit without trading there. There is no free lunch in stops - you are choosing which risk to keep.
## From submit to fill: the lifecycle
Send the order and it enters a state machine. It starts **pending** (submitted, not yet acknowledged), becomes **open** (accepted and resting in the book), and from there either fills - **partially filled** as liquidity arrives in pieces, then **complete** - or leaves by a side door: **cancelled** by you, or **rejected** by the broker or exchange for a margin, price-band, or risk-check failure. Modifying an order is just a controlled hop within this map: a price or quantity change re-submits the order and, on most venues, sends it to the back of the queue at the new price (we price that queue cost in the next chapter).
full fill Pending submitted Open resting in book Partially filled some lots done Complete terminal Rejected terminal Cancelled terminal accept fill fill rest reject cancel rest cancel The order state machine - every order lives somewhere on this map until it reaches a terminal state
Watch one order walk this map. The simulation below submits a 100-share buy limit and lets liquidity arrive in random chunks, recording the state at each step:
EX 2The lifecycle as a timelineNSEch19/02_lifecycle_timeline.py
Copy
```
# The order lifecycle as a state-machine timeline, from a small fill simulation.
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# The full state ladder of an exchange order; this run climbs the happy path.
LADDER = ["Rejected", "Cancelled", "Pending", "Open", "Partially filled", "Complete"]
ypos = {s: i for i, s in enumerate(LADDER)}

rng = np.random.default_rng(19)
QTY = 100                                   # a 100-share buy limit order
events = [(0.0, "Pending"), (0.4, "Open")]  # submitted, then acked and resting
t, filled = 0.4, 0
while filled < QTY:                          # liquidity arrives in random chunks
    t += float(rng.uniform(0.6, 1.4))
    filled = min(QTY, filled + int(rng.integers(20, 45)))
    events.append((round(t, 2), "Complete" if filled == QTY else "Partially filled"))

xs = [e[0] for e in events]
ys = [ypos[e[1]] for e in events]

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.step(xs, ys, where="post", color="#7c83ff", lw=2, zorder=2)
ax.scatter(xs, ys, color="#16a34a", s=60, zorder=3)
# Show the unrealised off-ramps every resting order faces.
ax.annotate("", xy=(0.4, ypos["Rejected"]), xytext=(0.0, ypos["Pending"]),
            arrowprops=dict(arrowstyle="->", color="#dc2626", ls="--", lw=1.2))
ax.annotate("", xy=(1.6, ypos["Cancelled"]), xytext=(0.4, ypos["Open"]),
            arrowprops=dict(arrowstyle="->", color="#dc2626", ls="--", lw=1.2))
ax.text(1.7, ypos["Cancelled"], " cancel / reject: terminal exits", va="center",
        color="#dc2626", fontsize=9)

ax.set_yticks(range(len(LADDER)))
ax.set_yticklabels(LADDER)
ax.set_xlabel("Seconds since submission")
ax.set_title(f"RELIANCE NSE  -  order lifecycle of a {QTY}-share buy limit")
ax.margins(x=0.05)

out = Path(__file__).with_suffix(".png")
plt.savefig(out, dpi=110, bbox_inches="tight")
print(f"Lifecycle: Pending -> Open -> Partially filled -> Complete in {xs[-1]:.2f}s, "
      f"{QTY}/{QTY} filled over {len(events) - 2} fills. Saved {out.name}")
```

Live output

```
Lifecycle: Pending -> Open -> Partially filled -> Complete in 2.80s, 100/100 filled over 3 fills. Saved 02_lifecycle_timeline.png
```

![The lifecycle as a timeline chart](https://openalgo.in/quant/charts/ch19_02_lifecycle_timeline.png)
In this run the order went pending to open to partially filled to complete in 2.80 seconds, filling all 100 shares across 3 separate fills. The red dashed off-ramps on the chart are the paths it did _not_ take this time but always could: a resting order can be cancelled, and a fresh order can be rejected at the door.
## The audit trail is your source of truth
Every one of those transitions is logged with a timestamp, an order id, and the price and quantity at that instant. This **audit trail** - surfaced in OpenAlgo as the order book and trade book - is not bureaucratic exhaust, it is the quant's ground truth. Your strategy logic believes it entered at 1314.15; the trade book knows you actually filled 60 shares at 1314.15 and 40 at 1314.20 a half-second later. That difference is **slippage** , and you cannot measure, attribute, or fix what you do not record. Reconcile every fill against what your model intended, every session, without exception.
Tip
Before sending anything live, run your order logic in OpenAlgo's sandbox (analyzer mode). It validates and routes orders through the same lifecycle and audit trail without touching a real exchange, so you can watch the state transitions and catch a malformed SL trigger or a wrong product type with zero risk.
## Who is allowed to trade: UCC and client-code controls
Behind every Indian order sits a **UCC** , the Unique Client Code that maps the order to a single PAN-verified account at the exchange. It is how the exchange knows _whose_ order this is, enforces position and margin limits, and runs surveillance. When you trade through an API, your orders are tagged to your client code and, under the SEBI framework for safer retail algorithmic trading (the circular dated 4 February 2025, which we revisit in the production module), routed with registered algo identifiers and key or static-IP controls. The practical point for a quant: your automated system is not anonymous. Every order is attributable, rate-limited, and risk-checked before it ever reaches the book.
Note
GTT and iceberg behave differently across venues. A GTT trigger is typically watched broker-side and only becomes a live exchange order once it trips, so it does not hold a queue position while it waits. Iceberg or disclosed-quantity orders refresh a new visible slice each time the current one fills, which means each slice rejoins the queue at the back. Know where your order actually rests before you rely on it.
## Product types decide what happens after the fill
One last field changes everything about a filled order: the **product type**.
  * **MIS** (intraday) gives you higher leverage but is auto-squared-off before the close. Hold nothing overnight.
  * **NRML** (normal) carries a futures or options position overnight at full margin.
  * **CNC** (cash-and-carry) takes delivery of equity into your account for as long as you like.


The _same_ buy of a stock is a fundamentally different trade under each tag - different margin, different overnight risk, different square-off behaviour. Choosing MIS when you meant CNC is a classic and expensive mistake.
We can now read the book and speak its language fluently. Next we go deeper into the single most valuable real estate in that book - your place in the queue - and put a precise rupee value on getting there first.
On this page
