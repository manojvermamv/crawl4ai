Chapters
Module D · HFT, Execution & Trading Technology - Chapter 33
# Order Book Reconstruction and Replay
Rebuilding the full limit order book from a feed of events, replaying a trading day deterministically, and using it to test execution.
NSE
What you'll learn
  * ·From events to a book
  * ·Add, modify, cancel, trade
  * ·Deterministic replay
  * ·Reconstruction pitfalls
  * ·Building a research dataset
  * ·Replay for execution testing


A market data feed does not hand you a tidy order book. It hands you a _firehose of events_ : an order added here, a quantity trimmed there, a cancel, a trade, thousands per second on a busy NIFTY option. The book you saw in chapter 18, that neat ladder of bids and asks, does not arrive ready-made. You have to _build_ it, event by event, and rebuild it the same way every time you replay history. That rebuild is **order book reconstruction** , and getting it exactly right is the difference between a research dataset you can trust and a pile of plausible-looking garbage. This chapter shows you how the book is assembled from raw events, why determinism matters so much, and how a faithful replay becomes a laboratory for testing execution.
## From a tape of events to a living book
Think of the exchange as broadcasting a **tape** : an ordered, timestamped sequence of messages describing every change to the book. Each message is small. Strung together in the right order, they reconstruct the full state of supply and demand at any instant. This is what an L3 feed (chapter 32) really is - not snapshots of the book, but the _deltas_ that move it. To know the book at 09:23:14.337, you start from the open and apply every event up to that moment.
The state you maintain is just a map of resting orders: each with a side, a price, a quantity, and an arrival sequence number that encodes its time priority (chapter 20). The top of book - best bid, best ask, the spread - is then a simple query over that map: the highest bid price, the lowest ask price, and the quantity resting at each.
Key idea
An order book is not a thing the exchange sends you. It is a _state_ you compute by folding an ordered stream of events. Same events, applied in the same order, must always yield the same book. That property is called **determinism** , and it is the whole game.
## The four events that rebuild everything
Almost every venue's protocol reduces to four message types, and a reconstruction engine is just a handler for each:
  * **Add** - a new resting order enters the book at a price and quantity. It joins the back of the queue at that price.
  * **Modify** - an existing order changes. A _quantity reduction_ usually keeps its place in the queue; a _price change or size increase_ sends it to the back, losing time priority. Your engine must model that rule, because queue position is money.
  * **Cancel** - an order leaves the book. The level shrinks; if it was the last order at the best price, the best bid or ask jumps to the next level.
  * **Trade** - an aggressor crosses the spread and consumes resting orders, best price first and earliest-order first within a price. A trade removes liquidity from the _opposite_ side of the book.

Event tape ADD a2 812.05 x250 ADD a4 812.05 x150 MODIFY b2 qty 700 CANCEL a1 TRADE BUY 200 Reconstruction engine orders = { oid: side, price, qty, seq } apply(event) -> new state match: best price, then FIFO Reconstructed top of book ask 812.10 x250 spread 0.10 bid 812.00 x700 a query over the order map Reconstruction: fold an ordered event tape through a state machine, then query the top of book
## Replaying the tape, deterministically
Let us build the engine and feed it a hand-built tape. The example below defines a tiny price-time-priority book - the same matching rules a real venue uses - and walks a deterministic sequence of sixteen events through it, printing the top of book after each one. The events are _synthetic_ , anchored to a stock trading near Rs 812 on a 5-paise tick, but the reconstruction logic is exactly what you would run over a real L3 feed. Nothing here is random; it is pinned so that you, and your future self, get byte-for-byte the same book every run.
EX 1Rebuild the top of book from an event tapeNSEch33/01_reconstruct_book.py
Copy
```
# Reconstruction demo: rebuild the top of book from a deterministic event tape.
# Events are SYNTHETIC, but the add/modify/cancel/trade replay logic is the real thing.
import random

random.seed(7)  # nothing random here, but pin the seed so the demo is reproducible


class OrderBook:
    """A tiny price-time-priority book rebuilt purely from events."""

    def __init__(self):
        self.orders = {}  # oid -> {side, price, qty, seq}
        self.seq = 0

    def add(self, oid, side, price, qty):
        self.seq += 1
        self.orders[oid] = {"side": side, "price": price, "qty": qty, "seq": self.seq}

    def modify(self, oid, price=None, qty=None):
        o = self.orders[oid]
        if price is not None and price != o["price"]:
            o["price"] = price            # a price change loses time priority
            self.seq += 1
            o["seq"] = self.seq
        if qty is not None:
            o["qty"] = qty

    def cancel(self, oid):
        self.orders.pop(oid, None)

    def trade(self, side, qty):
        # An aggressor of 'side' eats resting orders on the opposite side,
        # best price first, then earliest order (FIFO) at that price.
        opp = "S" if side == "B" else "B"
        resting = [o for o in self.orders.values() if o["side"] == opp]
        resting.sort(key=lambda o: (o["price"], o["seq"]) if side == "B"
                     else (-o["price"], o["seq"]))
        left = qty
        for o in resting:
            if left <= 0:
                break
            take = min(o["qty"], left)
            o["qty"] -= take
            left -= take
        self.orders = {k: v for k, v in self.orders.items() if v["qty"] > 0}

    def top(self):
        bids, asks = {}, {}
        for o in self.orders.values():
            lv = bids if o["side"] == "B" else asks
            lv[o["price"]] = lv.get(o["price"], 0) + o["qty"]
        bb = max(bids) if bids else None
        ba = min(asks) if asks else None
        return bb, (bids.get(bb, 0) if bb else 0), ba, (asks.get(ba, 0) if ba else 0)


# A hand-built deterministic tape, SBIN-like prices on a 0.05 paise tick.
TAPE = [
    ("add", "b1", "B", 811.95, 500), ("add", "a1", "S", 812.15, 400),
    ("add", "b2", "B", 812.00, 300), ("add", "a2", "S", 812.05, 250),
    ("add", "a3", "S", 812.10, 600), ("modify", "b2", None, 700),
    ("trade", "B", 200), ("add", "a4", "S", 812.05, 150),
    ("trade", "B", 200), ("cancel", "a1"),
    ("add", "b3", "B", 812.05, 400), ("trade", "S", 300),
    ("trade", "S", 100), ("cancel", "b1"),
    ("add", "a5", "S", 812.05, 350), ("trade", "B", 700),
]

book = OrderBook()
print(f"{'step':>4} {'event':<22} {'bid':>8}{'x':>6} {'|':^3} {'ask':<8}{'x':<6} {'spread':>7}")
for i, ev in enumerate(TAPE, 1):
    kind = ev[0]
    if kind == "add":
        book.add(ev[1], ev[2], ev[3], ev[4])
        label = f"add {ev[1]} {ev[2]} {ev[3]:.2f}x{ev[4]}"
    elif kind == "modify":
        book.modify(ev[1], ev[2], ev[3])
        label = f"modify {ev[1]} qty->{ev[3]}"
    elif kind == "cancel":
        book.cancel(ev[1])
        label = f"cancel {ev[1]}"
    else:
        book.trade(ev[1], ev[2])
        label = f"trade {ev[1]} {ev[2]}"
    bb, bq, ba, aq = book.top()
    bbs = f"{bb:.2f}" if bb is not None else "-"
    bas = f"{ba:.2f}" if ba is not None else "-"
    spr = f"{ba - bb:.2f}" if (bb is not None and ba is not None) else "-"
    print(f"{i:>4} {label:<22} {bbs:>8}{bq:>6} {'|':^3} {bas:<8}{aq:<6} {spr:>7}")

bb, bq, ba, aq = book.top()
print(f"\nReconstruction demo: replayed {len(TAPE)} events; "
      f"final top of book bid {bb:.2f} x{bq} / ask {ba:.2f} x{aq}, spread {ba - bb:.2f}.")
```

Live output

```
step event                       bid     x  |  ask     x       spread
   1 add b1 B 811.95x500      811.95   500  |  -       0            -
   2 add a1 S 812.15x400      811.95   500  |  812.15  400       0.20
   3 add b2 B 812.00x300      812.00   300  |  812.15  400       0.15
   4 add a2 S 812.05x250      812.00   300  |  812.05  250       0.05
   5 add a3 S 812.10x600      812.00   300  |  812.05  250       0.05
   6 modify b2 qty->700       812.00   700  |  812.05  250       0.05
   7 trade B 200              812.00   700  |  812.05  50        0.05
   8 add a4 S 812.05x150      812.00   700  |  812.05  200       0.05
   9 trade B 200              812.00   700  |  812.10  600       0.10
  10 cancel a1                812.00   700  |  812.10  600       0.10
  11 add b3 B 812.05x400      812.05   400  |  812.10  600       0.05
  12 trade S 300              812.05   100  |  812.10  600       0.05
  13 trade S 100              812.00   700  |  812.10  600       0.10
  14 cancel b1                812.00   700  |  812.10  600       0.10
  15 add a5 S 812.05x350      812.00   700  |  812.05  350       0.05
  16 trade B 700              812.00   700  |  812.10  250       0.10

Reconstruction demo: replayed 16 events; final top of book bid 812.00 x700 / ask 812.10 x250, spread 0.10.
```

Read the output as a story. The book opens one-sided (a lone bid, no ask yet), then a sell order arrives and a spread of 0.20 appears. A tighter bid and ask narrow it to 0.05. A trade for 200 eats the best ask down to 50 lots resting; a second trade clears that level entirely and the best ask jumps from 812.05 up to 812.10, widening the spread to 0.10. After all sixteen events the book settles at **bid 812.00 for 700 against ask 812.10 for 250, a spread of 0.10**. Every one of those numbers is computed, not typed - which is precisely the discipline reconstruction demands.
Tip
Always store an **arrival sequence number** on every order. Two orders can rest at the same price; the only thing that decides who fills first is who got there first. Throw that away and your fills will be wrong even though your prices look right.
## Where reconstruction goes wrong
Reconstruction is unforgiving because errors _compound_. Apply one event wrong and every later book is corrupted. The classic failure modes:
  * **Out-of-order or dropped messages.** Feeds can deliver packets late, duplicated, or not at all (chapter 32). Apply a cancel before its add and your state desynchronises. Real engines use sequence numbers to detect gaps and a _snapshot plus deltas_ protocol to resynchronise: periodically the venue sends a full book snapshot you can anchor to.
  * **The opening cross.** The pre-open auction sets the first price through a different mechanism. If you start your replay mid-stream without the opening snapshot, your book is missing its foundation.
  * **Hidden and iceberg quantity.** Disclosed-quantity orders show only a slice of their true size. Your reconstructed depth will understate the real liquidity, and a trade can print larger than any visible order. Model the refresh or you will mis-measure depth.
  * **Self-trade and amend semantics.** Does a quantity increase keep or lose priority? Does a modify cancel-and-replace or amend in place? These rules are venue-specific. Guess wrong and your queue-position model is fiction.


Heads up
A reconstructed book that _looks_ sensible can still be silently wrong. Validate it: after each event, the best bid must stay below the best ask (no crossed or locked book), quantities must be non-negative, and your reconstructed trades must reconcile against the venue's published trade tape. If they do not match, your engine has a bug, not the exchange.
## A dataset you can actually trust
Once your engine is faithful, you turn the tape into research data. For each event - or sampled at a fixed cadence - you snapshot features that downstream models consume: the spread, the depth at each level, the order-book imbalance, the microprice, the trade sign and size. Store these as a time-indexed table and you have the raw material for the microstructure signals of Module G and the impact models of chapter 26.
The non-negotiable rule is **point-in-time honesty**. Every feature at time _t_ must be computable from events at or before _t_ , never after. It is dangerously easy to leak the future when you have the whole tape in memory - to label a trade with a price that only existed two events later. Reconstruction done right is the cleanest defence against the look-ahead bias we attack head-on in chapter 68.
## Replay as an execution lab
The same engine that builds research data becomes a **simulator** for execution. Replay the tape and inject your own order into the reconstructed book. Now you can ask the questions that decide whether a strategy survives contact with the market: if I had joined the bid at 812.00, how many lots were ahead of me, and did the queue drain far enough to fill me before the price moved? If I had crossed with a market order, how many levels would I have eaten and what was my average fill versus the mid?
The chart below replays our synthetic tape and plots the best bid, the best ask and the spread across the event sequence, so you can _see_ the book breathe as liquidity arrives and trades consume it.
EX 2Replay the book and watch the spread breatheNSEch33/02_replay_spread.py
Copy
```
# Replay the reconstructed book and plot best bid, best ask and the spread per event.
import random
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

random.seed(7)  # pinned for a reproducible deterministic replay


class OrderBook:
    """Same price-time-priority book as example 01, rebuilt from events."""

    def __init__(self):
        self.orders = {}
        self.seq = 0

    def add(self, oid, side, price, qty):
        self.seq += 1
        self.orders[oid] = {"side": side, "price": price, "qty": qty, "seq": self.seq}

    def modify(self, oid, price=None, qty=None):
        o = self.orders[oid]
        if price is not None and price != o["price"]:
            o["price"] = price
            self.seq += 1
            o["seq"] = self.seq
        if qty is not None:
            o["qty"] = qty

    def cancel(self, oid):
        self.orders.pop(oid, None)

    def trade(self, side, qty):
        opp = "S" if side == "B" else "B"
        resting = [o for o in self.orders.values() if o["side"] == opp]
        resting.sort(key=lambda o: (o["price"], o["seq"]) if side == "B"
                     else (-o["price"], o["seq"]))
        left = qty
        for o in resting:
            if left <= 0:
                break
            take = min(o["qty"], left)
            o["qty"] -= take
            left -= take
        self.orders = {k: v for k, v in self.orders.items() if v["qty"] > 0}

    def top(self):
        bids, asks = {}, {}
        for o in self.orders.values():
            lv = bids if o["side"] == "B" else asks
            lv[o["price"]] = lv.get(o["price"], 0) + o["qty"]
        bb = max(bids) if bids else None
        ba = min(asks) if asks else None
        return bb, ba


TAPE = [
    ("add", "b1", "B", 811.95, 500), ("add", "a1", "S", 812.15, 400),
    ("add", "b2", "B", 812.00, 300), ("add", "a2", "S", 812.05, 250),
    ("add", "a3", "S", 812.10, 600), ("modify", "b2", None, 700),
    ("trade", "B", 200), ("add", "a4", "S", 812.05, 150),
    ("trade", "B", 200), ("cancel", "a1"),
    ("add", "b3", "B", 812.05, 400), ("trade", "S", 300),
    ("trade", "S", 100), ("cancel", "b1"),
    ("add", "a5", "S", 812.05, 350), ("trade", "B", 700),
]

book = OrderBook()
steps, bids, asks, spreads = [], [], [], []
for i, ev in enumerate(TAPE, 1):
    kind = ev[0]
    if kind == "add":
        book.add(ev[1], ev[2], ev[3], ev[4])
    elif kind == "modify":
        book.modify(ev[1], ev[2], ev[3])
    elif kind == "cancel":
        book.cancel(ev[1])
    else:
        book.trade(ev[1], ev[2])
    bb, ba = book.top()
    if bb is None or ba is None:
        continue
    steps.append(i)
    bids.append(bb)
    asks.append(ba)
    spreads.append(round(ba - bb, 2))

sns.set_theme(style="whitegrid")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.5, 5.4), sharex=True,
                               gridspec_kw={"height_ratios": [2, 1]})
ax1.step(steps, asks, where="post", color="#dc2626", label="Best ask", linewidth=1.8)
ax1.step(steps, bids, where="post", color="#16a34a", label="Best bid", linewidth=1.8)
ax1.fill_between(steps, bids, asks, step="post", color="#7c83ff", alpha=0.12)
ax1.set_ylabel("Price")
ax1.set_title("Reconstructed top of book replayed event by event (synthetic tape)")
ax1.legend(loc="upper left")
ax2.step(steps, spreads, where="post", color="#7c83ff", linewidth=1.8)
ax2.fill_between(steps, 0, spreads, step="post", color="#7c83ff", alpha=0.15)
ax2.set_ylabel("Spread")
ax2.set_xlabel("Event number on the tape")

out = Path(__file__).with_suffix(".png")
plt.savefig(out, dpi=110, bbox_inches="tight")
print(f"Replayed {len(TAPE)} events; spread moved between {min(spreads):.2f} and "
      f"{max(spreads):.2f}, best ask {asks[0]:.2f} -> {asks[-1]:.2f}. Saved {out.name}")
```

Live output

```
Replayed 16 events; spread moved between 0.05 and 0.20, best ask 812.15 -> 812.10. Saved 02_replay_spread.png
```

![Replay the book and watch the spread breathe chart](https://openalgo.in/quant/charts/ch33_02_replay_spread.png)
Over the run the **spread moves between 0.05 and 0.20** while the best ask walks from 812.15 down to 812.10 - small numbers, but on a real book these are exactly the moments where a passive fill is won or lost. A replay that honours queue priority and only reacts to information available at each instant is the most honest backtest of execution you can build. It is the foundation the market-making and impact chapters (ch38, ch26) stand on.
Note
Replaying your _own_ orders against a historical tape has a built-in limitation: your order would have changed the future. A passive bid that fills removes liquidity others might have taken; an aggressive order moves the price for everyone after you. Replay is excellent for queue-position and cost questions and weak for large, market-moving orders. Know which question you are asking.
With a deterministic engine, a validated dataset and a replay lab, you can finally test the fast strategies that live and die inside the order book. The next chapter opens that world: the families of high-frequency strategy - market making, arbitrage and event reaction - and the very different edges and risks each one carries.
On this page
