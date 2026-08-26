Chapters
Module D · HFT, Execution & Trading Technology - Chapter 31
# DMA, Co-Location and Low-Latency Access
The microstructure of speed - direct market access, co-location at NSE, tick-by-tick feeds, timestamping and the latency arms race.
NSE
What you'll learn
  * ·Direct market access
  * ·Co-location at NSE/BSE
  * ·Tick-by-tick data
  * ·Latency arbitrage
  * ·Timestamping and clocks
  * ·Where retail can and cannot play


In the time it takes you to blink, a high-frequency trading firm has placed, modified and cancelled thousands of orders. HFT is the part of the market that feels like science fiction - and the part most likely to make a new quant feel hopeless, as if the game is rigged by people with faster computers. The truth is more useful than that fear. By the end of this chapter you'll understand exactly what speed buys, why you can't win that race - and why you don't have to. This is the last piece of microstructure, and it's strangely liberating.
## What HFT actually does
Strip away the mystique and HFT is just three familiar activities done _very_ fast and fully automated:
  * **Market making** - quoting both bid and ask on thousands of instruments, earning the spread, managing inventory in microseconds (the professional version of Module C's liquidity provision).
  * **Latency arbitrage** - spotting that the same instrument is momentarily cheaper on one venue than another and trading the gap before it closes.
  * **Statistical arbitrage at speed** - the pairs and index-arb ideas of Module G, but acting on fleeting micro-dislocations that vanish in milliseconds.


None of it is magic or fortune-telling. It's the same logic you're learning, executed faster than a human can perceive - which is exactly why it lives in a world you can't enter on speed alone.
## The speed spectrum
Every participant sits somewhere on a spectrum of speed, and the distances are staggering:
← FASTER SLOWER → HFT colocated ~microseconds Prop desk ~1 millisecond Retail algo (you) ~hundreds of ms Human ~seconds The speed spectrum - and where a retail quant really sits
The gap between HFT and you isn't a little - it's a _factor of tens of thousands_. And it isn't a fair fight you could win with a better laptop, because at this level the limit is **physics** : the speed of light through a cable, the length of the wire to the matching engine. Let's prove your place on that line with real data.
## Measure your own latency
Don't take it on faith - time your own round trip to the market:
EX 1Timing your round tripNSEch31/01_measure_latency.py
Copy
```
# How fast is YOUR setup? Time a round trip to the market and compare to HFT.
import os
import statistics
import time

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

latencies = []
for _ in range(20):
    t0 = time.perf_counter()
    client.quotes(symbol="RELIANCE", exchange="NSE")     # one round trip to the market
    latencies.append((time.perf_counter() - t0) * 1000)  # in milliseconds
    time.sleep(0.6)                                       # space calls out so rate limits don't skew the timing

latencies.sort()
p95 = latencies[int(len(latencies) * 0.95) - 1]
print(f"Round trips : {len(latencies)}")
print(f"Fastest     : {min(latencies):.1f} ms")
print(f"Median      : {statistics.median(latencies):.1f} ms")
print(f"95th pct    : {p95:.1f} ms")
print(f"Slowest     : {max(latencies):.1f} ms")
print("\nAn HFT firm colocated at the exchange measures this in MICROSECONDS - thousands of times faster.")
```

Live output

```
Round trips : 20
Fastest     : 32.2 ms
Median      : 500.1 ms
95th pct    : 2191.6 ms
Slowest     : 2247.8 ms

An HFT firm colocated at the exchange measures this in MICROSECONDS - thousands of times faster.
```

Your _fastest_ call might be a few tens of milliseconds, but typical round trips run into the hundreds - and notice the slow ones, where the broker's **rate limits** deliberately throttle you. That's a second wall: a retail API won't even _let_ you poll quickly, by design. Whatever your number, compare it to an HFT engine's _microseconds_. You're not a little behind; you're in a different universe of time.
## The shape of your latency
Plot every sample and your latency has a distinct, lumpy shape - a fast cluster, then a long tail where throttling and the network bite:
EX 2The shape of your latencyNSEch31/02_latency_chart.py
Copy
```
# Your latency has a shape - plot it, and see how far it is from HFT speed.
import os
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

latencies = []
for _ in range(40):
    t0 = time.perf_counter()
    client.quotes(symbol="RELIANCE", exchange="NSE")
    latencies.append((time.perf_counter() - t0) * 1000)
    time.sleep(0.6)        # space calls out so rate limits don't skew the timing

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(8, 4.5))
sns.histplot(latencies, bins=25, color="#7c83ff", edgecolor="none", ax=ax)
med = sorted(latencies)[len(latencies) // 2]
ax.axvline(med, color="#16a34a", lw=1.6, label=f"your median {med:.1f} ms")
ax.axvline(0.01, color="#dc2626", lw=1.6, ls="--", label="HFT colocated ~0.01 ms")
ax.set_title("Your round-trip latency vs HFT speed")
ax.set_xlabel("Round-trip latency (milliseconds)")
ax.set_ylabel("Count")
ax.legend()

out = Path(__file__).with_suffix(".png")
plt.savefig(out, dpi=110, bbox_inches="tight")
print(f"Median {med:.1f} ms - roughly {med / 0.01:,.0f}x slower than a colocated HFT engine. Saved {out.name}")
```

Live output

```
Median 499.9 ms - roughly 49,988x slower than a colocated HFT engine. Saved 02_latency_chart.png
```

![The shape of your latency chart](https://openalgo.in/quant/charts/ch31_02_latency_chart.png)
The red line marks HFT's colocated speed - so far to the left of your distribution it's practically at zero. No amount of code optimisation on your side moves your cloud of dots anywhere near it. The race is over before it starts.
## Colocation and the arms race
How do HFT firms get to microseconds? **Colocation** - they rent rack space for their servers _inside_ the exchange's own data centre, a few metres of cable from the matching engine. NSE and BSE both offer it. From there, the competition becomes absurd and literal: shaving nanoseconds by shortening cables, using faster network cards, even choosing a rack closer to the engine. They consume **tick-by-tick** data feeds (every single order and trade, not the throttled snapshots you get) and react in hardware. It's a genuine arms race, and the price of entry is crores.
Heads up
This is why **latency-sensitive strategies are off-limits to retail**. Any edge that depends on being first - sub-second arbitrage, sniping a stale quote, reacting to a print before others - belongs to the colocated firms. If your strategy's profit comes from _speed_ , you will lose. Build nothing that races them.
## Where a retail quant can - and can't - play
Here's the liberating part. Speed is just _one_ axis of competition, and HFT dominates only that one. You compete on the axes they ignore:
  * **Time horizon.** HFT lives in microseconds and holds for milliseconds. Hold for _days or weeks_ and their speed advantage is completely irrelevant - a swing or positional edge doesn't care who was 10 microseconds faster.
  * **Research depth.** A better _signal_ - a real, well-validated edge (Modules C-G) - beats a faster _connection_ when the holding period is long.
  * **Niches and capacity.** HFT needs liquid, high-volume instruments to deploy capital at speed. Smaller, slower, less crowded corners of the market are often beneath their notice - and open to you.


Key idea
You will never win on speed, so don't try. Win on **horizon, research and patience** - edges that take minutes, hours or days to play out, where being thoughtful beats being fast. Almost everything in the rest of this course is built for exactly that game.
## Try it yourself
  * Run the latency example at a quiet time and a busy market hour. Does your median round trip get slower when the market is active?
  * Look up the cost of an NSE colocation rack and a tick-by-tick data feed. Roughly how large would a strategy have to be to justify that fixed cost?
  * List your own strategy ideas and mark each "speed-sensitive" or "horizon-based". The horizon-based ones are the ones worth your time.


## Recap
  * **HFT** is ordinary market-making, arbitrage and stat-arb done in **microseconds** , fully automated - fast, not magic.
  * The **speed spectrum** runs from HFT (microseconds) through prop desks (~1 ms) to retail algos (hundreds of ms) and humans (seconds) - a gap of _tens of thousands of times_ , limited by physics.
  * Measuring your own round trip proves it: you're in the **hundreds of milliseconds** , and broker **rate limits** stop you polling fast anyway.
  * **Colocation** (servers inside the exchange) and tick-by-tick feeds power the arms race - and put all latency-sensitive strategies out of retail reach.
  * You compete not on speed but on **time horizon, research depth and overlooked niches** - which is exactly what the rest of this course builds.


That completes Module C - market microstructure, from the order book to the speed of light. We now leave the plumbing behind and pick up the quant's other essential toolkit: the **mathematics of markets**. Next, we confront what returns actually look like, and why their fat-tailed reality breaks the neat assumptions of classical finance.
On this page
