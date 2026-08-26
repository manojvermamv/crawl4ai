Chapters
Module D · HFT, Execution & Trading Technology - Chapter 35
# Order-to-Trade Ratio, Cancellations and Quote Stuffing
The exchange's brakes on speed - the order-to-trade ratio, cancellation penalties, and the line between legitimate quoting and manipulative quote stuffing.
NSE
What you'll learn
  * ·The order-to-trade ratio
  * ·OTR penalties on NSE
  * ·Cancellation economics
  * ·Quote stuffing and spoofing
  * ·Layering and surveillance
  * ·Staying on the right side


A market maker's screen is a blur. In a single second its server can place, modify and cancel hundreds of quotes, chasing fair value as the book breathes. Almost none of those messages ever become a trade - they are cancelled and replaced microseconds later. The exchange sees every one of them, and it keeps a running count. Divide the orders by the trades and you get a number that quietly governs the entire fast end of the market: the **order-to-trade ratio**. Run it too high and you stop being a liquidity provider in the exchange's eyes and start being a cost on its matching engine - and the penalties begin. This chapter is about that number, the economics behind it, and the line between legitimate quoting and the manipulation that shares its mechanics.
## What the order-to-trade ratio measures
The **order-to-trade ratio (OTR)** is exactly what it says: the count of order messages a participant sends, divided by the number of trades those messages produce, over some window (usually a day, per symbol, per segment). The numerator is not just fresh orders - it includes **modifications and cancellations** , because each one is a message the matching engine must process. A maker that places a bid, nudges it up three times, then pulls it has sent four or five messages for zero trades.
Why would an exchange care? Because matching-engine capacity is finite and shared. Every message consumes bandwidth, CPU and bandwidth on the public data feed that everyone downstream must parse. A participant who floods the book with orders that never trade imposes a real cost on the system and on slower participants, while contributing little genuine liquidity. The OTR is the exchange's blunt-but-effective governor on that behaviour.
Note
OTR counts _messages_ , not just orders. New order, modify, cancel - each is one unit in the numerator. Trades are the denominator. A ratio of 50:1 means fifty messages reached the engine for every one that resulted in a fill.
A genuine two-sided maker naturally runs an OTR well above one. It re-quotes constantly to stay near fair value and to dodge **adverse selection** (getting filled only when the price is about to move against it). Let us measure that natural ratio on a real tape rather than guess it.
EX 1The OTR of an honest market makerNSEch35/01_order_to_trade_ratio.py
Copy
```
# Order-to-trade ratio of an honest two-sided market maker on a real price tape.
import os

import numpy as np
from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# The real intraday tape sets the re-quote and fill rhythm.
df = client.history(symbol="RELIANCE", exchange="NSE", interval="1m",
                    start_date="2026-06-23", end_date="2026-06-27")
close = df["close"].dropna()

# A two-sided maker cancels and replaces both quotes every time the mid moves.
move = close.diff().fillna(0.0)
requotes = int((move != 0).sum())          # one re-quote event per mid change
order_msgs = 2 * requotes                   # bid and ask each refreshed

# Fills land at turning points: a resting bid is hit on a dip, an ask on a pop.
sign = np.sign(move.values)
nz = sign[sign != 0]
turns = int((np.diff(nz) != 0).sum())
rng = np.random.default_rng(7)              # not every turn reaches the front of our queue
fills = int(rng.binomial(turns, 0.6))

otr = order_msgs / max(fills, 1)
THRESHOLD = 50.0                            # illustrative band; real slabs are exchange-set and revised
headroom = THRESHOLD / otr

print(f"RELIANCE 1m tape : {len(close)} bars, {requotes} mid moves, {fills} fills")
print(f"Order messages   : {order_msgs}   Trades : {fills}")
print(f"Order-to-trade   : {otr:.1f} : 1   (illustrative penalty band starts near {THRESHOLD:.0f}:1)")
status = "within limits" if otr < THRESHOLD else "IN PENALTY ZONE"
print(f"Status: {status} - room for {headroom:.1f}x more order messages per fill before the band trips.")
```

Live output

```
RELIANCE 1m tape : 1125 bars, 1006 mid moves, 311 fills
Order messages   : 2012   Trades : 311
Order-to-trade   : 6.5 : 1   (illustrative penalty band starts near 50:1)
Status: within limits - room for 7.7x more order messages per fill before the band trips.
```

On a real session of RELIANCE one-minute bars - 1,125 bars with 1,006 mid moves and 311 modelled fills - the honest maker sends 2,012 order messages and trades 311 times, for an order-to-trade ratio of **6.5 : 1**. That is the cost of staying at fair value: it re-quotes both sides every time the mid ticks, but only a fraction of those quotes ever get hit. Against an illustrative penalty band near 50:1, the maker has comfortable headroom - room for roughly **7.7x** more messaging per fill before it would trip the line. Honest making is messaging-heavy, but nowhere near the danger zone.
## Why exchanges cap it
The Indian exchanges run an explicit OTR framework. The structure is what matters and it is consistent across venues: the exchange measures your messages-per-trade per symbol per day, allows a free band for normal activity, and then levies an **incremental, slab-based charge** that rises the deeper into high-ratio territory you go. Bona fide registered market makers in approved schemes get relief, because their job is to quote. Everyone else pays for noise.
Heads up
The exact OTR slabs, the free band and the per-message charges are set by each exchange's circulars and are revised periodically. Do not hard-code a number from a blog post. Read the current circular for the segment you trade. Treat any figure in this chapter - including the 50:1 band in the examples - as illustrative of the _structure_ , not a live threshold.
The design is deliberately progressive. A modest OTR costs nothing. A high but explicable OTR costs a little. A pathological OTR - tens of thousands of messages per trade - costs enough to make the strategy uneconomic. The exchange is not trying to ban quoting; it is pricing the externality so that messaging stays roughly proportional to genuine trading interest.
## The economics of cancellation
Here is the uncomfortable truth that makes OTR rules necessary: **cancelling an order is almost free**. There is no exchange fee to pull a resting limit order, no capital tied up once it is gone, no market risk on an order that never filled. For a colocated engine, sending a cancel-replace pair costs a few microseconds. Left unpriced, the rational move is to quote aggressively and cancel relentlessly - to use the order book as a probe rather than a commitment.
The OTR penalty is what puts a price on that free action. It turns "cancellation is free" into "cancellation is free until your ratio crosses the band, then every extra message has a cost." A serious maker therefore runs a **messaging budget** : it decides how many order messages it can spend per fill and tunes its quoting logic - how often it re-prices, how tight it quotes, how it skews on inventory (Module D, ch38) - to stay inside that budget while still avoiding adverse selection.
The order-to-trade meter WITHIN LIMITS PENALTY ZONE penalty band ~50:1 (exchange-set, revised) 0 25 75 100 honest maker 6.5:1 quote stuffing 76:1 order messages per trade → An honest maker sits low; stuffing drives the needle into the penalty zone
The meter makes the regime visible. Honest quoting lives in the green at a single-digit ratio. Push messaging far enough beyond genuine trading and the needle crosses into the red, where the exchange's charges - and its surveillance - are waiting.
## Quote stuffing, spoofing and layering
Beyond the cost externality lies the real reason regulators watch the ratio: the same mechanics power outright manipulation. Three patterns matter, and all three are prohibited under SEBI's Prohibition of Fraudulent and Unfair Trade Practices (PFUTP) Regulations.
  * **Quote stuffing** is flooding a symbol with a huge number of orders and instant cancels, with no intent to trade. The goal is to slow down or confuse competitors by clogging the data feed and the engine, buying the stuffer a latency edge. It produces an enormous OTR and almost no fills.
  * **Spoofing** is placing large, visible orders on one side that you never intend to execute, to create a false impression of supply or demand, then cancelling them once the price has moved your way and trading the other side. The spoof order is bait.
  * **Layering** is spoofing's organised cousin: stacking several non-bona-fide orders at multiple price levels to manufacture the appearance of deep one-sided interest, again to nudge the price before trading against the illusion.


The tell for all three is the same statistical fingerprint: messages vastly out of proportion to trades, with cancels clustered right before or after a price move. The next example contrasts the message profile of honest making with a stuffing profile on the same real tape.
EX 2Healthy quoting vs a stuffing profileNSEch35/02_otr_profiles.py
Copy
```
# Running order-to-trade ratio: an honest maker vs a quote-stuffing profile.
import os
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

df = client.history(symbol="RELIANCE", exchange="NSE", interval="1m",
                    start_date="2026-06-23", end_date="2026-06-27")
close = df["close"].dropna()
move = close.diff().fillna(0.0)

# Honest maker: two order messages per real mid move, fills at turning points.
honest_orders = 2 * (move != 0).to_numpy().astype(float)
sign = np.sign(move.to_numpy())
turn = np.zeros(len(close))
nz_idx = np.flatnonzero(sign != 0)
flip = nz_idx[1:][np.diff(sign[nz_idx]) != 0]
turn[flip] = 1.0
rng = np.random.default_rng(7)
fills = turn * (rng.random(len(close)) < 0.6)

# Stuffing profile: same fills, plus a flood of phantom quotes cancelled in microseconds.
phantom = rng.poisson(20, len(close)).astype(float)
stuff_orders = honest_orders + phantom

cum_fills = np.maximum(np.cumsum(fills), 1)
otr_honest = np.cumsum(honest_orders) / cum_fills
otr_stuff = np.cumsum(stuff_orders) / cum_fills

THRESHOLD = 50.0
warm = int(np.argmax(np.cumsum(fills) >= 5))   # skip the noisy small-denominator warm-up
x = np.arange(len(close))[warm:]
sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(8.4, 4.6))
ax.axhspan(THRESHOLD, otr_stuff[warm:].max() * 1.10,
           color="#dc2626", alpha=0.10)
ax.axhline(THRESHOLD, color="#dc2626", lw=1.4, ls="--",
           label=f"illustrative penalty band ~{THRESHOLD:.0f}:1")
ax.plot(x, otr_honest[warm:], color="#16a34a", lw=1.8, label="honest maker")
ax.plot(x, otr_stuff[warm:], color="#7c83ff", lw=1.8, label="quote-stuffing profile")
ax.set_title("Running order-to-trade ratio: honest making vs quote stuffing")
ax.set_xlabel("Minute bar of the session window")
ax.set_ylabel("Cumulative order-to-trade ratio")
ax.legend(loc="center right")

out = Path(__file__).with_suffix(".png")
plt.savefig(out, dpi=110, bbox_inches="tight")
print(f"Honest OTR settles at {otr_honest[-1]:.1f}:1; stuffing profile ends at "
      f"{otr_stuff[-1]:.1f}:1, deep in the penalty zone. Saved {out.name}")
```

Live output

```
Honest OTR settles at 6.2:1; stuffing profile ends at 76.2:1, deep in the penalty zone. Saved 02_otr_profiles.png
```

![Healthy quoting vs a stuffing profile chart](https://openalgo.in/quant/charts/ch35_02_otr_profiles.png)
The running ratio tells the story cleanly. The honest maker settles at **6.2 : 1** and stays flat near the floor for the whole session. The stuffing profile - the same fills, plus a constant flood of phantom quotes cancelled in microseconds - climbs to **76.2 : 1** and lives the entire session inside the shaded penalty zone above the 50:1 band. Crucially, both profiles trade the _same amount_. The only difference is the cloud of messages that never become trades, and that difference is precisely what the OTR is built to expose.
Heads up
Quote stuffing, spoofing and layering are not aggressive trading - they are market manipulation, and they have drawn enforcement action and disgorgement in India and abroad. An OTR penalty is a fee; a PFUTP finding is a regulatory case. Never build a strategy whose edge comes from misleading the book.
## Surveillance and staying compliant
Exchanges and SEBI run automated surveillance over every message you send. The OTR framework is the visible part - a daily charge - but behind it sit pattern detectors that flag clustered cancels around price moves, abnormal message bursts, and order books that show depth which evaporates on approach. Your **audit trail** - every order, modify and cancel timestamped to your client code and algo ID - is retained and reconstructable, the same event stream we discussed for order-book replay in ch33. There is no anonymity in the message log.
Staying clean is mostly discipline, not cleverness:
  * **Budget your messaging.** Set a target OTR for each instrument and have your engine throttle re-quoting before it breaches the band. Recall from ch31 that broker rate limits already cap your message rate; treat them as a floor of good behaviour, not a ceiling to fight.
  * **Cancel for real reasons.** Re-quote because fair value moved or inventory changed, not to probe or to paint the book. Every cancel should have an explanation you would be comfortable showing a surveillance team.
  * **Register and label your algos.** Under the retail API algo framework (ch39), your orders carry a registered algo ID. That traceability is a feature: it lets you prove your intent was bona fide.


Key idea
The order-to-trade ratio is the single number that separates a liquidity provider from a load on the system. Keep it proportional to your real trading, cancel only with genuine cause, and you stay on the right side of both the fee schedule and the law.
Tip
Before going live, log your strategy's own OTR per symbol in the sandbox (analyzer mode in OpenAlgo) and watch it across a full session. If it drifts upward without a matching rise in fills, your re-quoting logic is leaking messages - fix it before an exchange charge or a surveillance alert finds it for you.
OTR discipline keeps your messaging honest on a single venue. But serious execution rarely lives on one venue at a time. Next, in ch36, we route a single order across NSE and BSE at once - smart order routing, the consolidated book, and the best-execution duty that decides where each child order should go.
On this page
