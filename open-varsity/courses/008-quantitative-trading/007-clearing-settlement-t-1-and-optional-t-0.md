Chapters
Module A · Quant Career Map & Indian Market Structure - Chapter 07
# Clearing, Settlement, T+1 and Optional T+0
The life of a trade after the match - novation, netting, margins through the day, the T+1 cycle and India's optional T+0 settlement.
NSE
What you'll learn
  * ·Trade life cycle after matching
  * ·Novation and netting
  * ·Settlement obligations
  * ·The T+1 cycle
  * ·Optional T+0 settlement
  * ·Settlement risk and a quant


In the last chapter we watched a single click travel from your screen to the demat vault and back. That was the map. Now we descend into the engine room, because the few hours _between_ a match and a settlement are where a surprising amount of a quant's real economics is decided. Carry, funding, corporate-action risk, the leverage your broker can extend, even why a short can blow up on you - all of it lives in the mechanics of clearing and settlement. This is the least glamorous chapter in Module A and one of the most quietly important. Let's earn it.
## Novation: the clearing corp becomes your counterparty
The instant the exchange matches your buy against some stranger's sell, something legally radical happens. The clearing corporation steps into the middle and performs **novation** - it tears up the single contract between you and the stranger and replaces it with _two_ contracts: one where the clearing corp is the seller to you, and one where it is the buyer from the stranger. You now face the clearing corporation, and so does everyone else. The original counterparty has vanished from your risk picture entirely.
This is the deepest idea in market structure. A **central counterparty (CCP)** - the clearing corporation acting in this role - is what lets millions of anonymous strangers trade without doing credit checks on each other. You never have to ask "is the person on the other side good for it?" because you are not, after novation, facing that person at all.
But novation does not make risk disappear. It _concentrates_ it. Every participant's counterparty risk is now pointed at one institution. If the CCP ever failed, the whole market would fail with it. That is precisely why a clearing corporation is wrapped in the most conservative risk machinery in all of finance, which we will reach at the end of this chapter.
Key idea
Novation replaces "you versus a stranger" with "you versus the clearing corporation" on every single trade. It does not erase counterparty risk - it _mutualises_ and concentrates it into one fortress-grade institution, funded by everyone's margins.
## Multilateral netting: thousands of trades, one obligation
Here is the second piece of magic, and it is where settlement actually gets cheap. Because the clearing corp is now the counterparty to _every_ leg, it can do something no bilateral arrangement could: add them all up. This is **multilateral netting**. Across a whole day of frantic trading in one security, the CCP nets every member's buys against their sells and produces just two numbers per security per member: a single **securities obligation** (net shares to deliver or receive) and a single **funds obligation** (net cash to pay or receive).
Watch how violently that compresses a real day of churning:
EX 1Many gross trades net to one obligationNSEch07/01_netting_simulation.py
Copy
```
# Multilateral netting: many gross trades collapse to ONE settlement obligation.
import os
from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# A day-trader churns RELIANCE all session. Use real 15m bars from one day,
# one trade per bar: buy a green bar, sell a red bar, fixed 100 shares each.
day = "2026-06-25"
bars = client.history(symbol="RELIANCE", exchange="NSE", interval="15m",
                      start_date=day, end_date=day)
qty = 100

buy_qty = buy_val = sell_qty = sell_val = 0
gross_turnover = 0.0
for _, b in bars.iterrows():
    price = float(b["close"])
    gross_turnover += price * qty
    if b["close"] >= b["open"]:
        buy_qty += qty
        buy_val += price * qty
    else:
        sell_qty += qty
        sell_val += price * qty

net_qty = buy_qty - sell_qty                 # single securities obligation
net_funds = sell_val - buy_val               # single funds obligation (+receive / -pay)
side = "RECEIVE" if net_funds >= 0 else "PAY"

print(f"RELIANCE {day}: {len(bars)} gross trades simulated from real 15m bars")
print(f"  Bought {buy_qty} sh for Rs {buy_val:,.0f} | Sold {sell_qty} sh for Rs {sell_val:,.0f}")
print(f"  Gross turnover that crossed the tape: Rs {gross_turnover:,.0f}")
print(f"  Settled trade-by-trade that is {len(bars)} separate obligations")
print(f"  After multilateral netting: deliver/receive {net_qty:+d} shares, "
      f"{side} Rs {abs(net_funds):,.0f} - ONE obligation")
print(f"Netting compressed Rs {gross_turnover:,.0f} of gross flow into a single "
      f"Rs {abs(net_funds):,.0f} settlement ({abs(net_funds)/gross_turnover*100:.1f}% of gross).")
```

Live output

```
RELIANCE 2026-06-25: 25 gross trades simulated from real 15m bars
  Bought 1100 sh for Rs 1,455,110 | Sold 1400 sh for Rs 1,849,120
  Gross turnover that crossed the tape: Rs 3,304,230
  Settled trade-by-trade that is 25 separate obligations
  After multilateral netting: deliver/receive -300 shares, RECEIVE Rs 394,010 - ONE obligation
Netting compressed Rs 3,304,230 of gross flow into a single Rs 394,010 settlement (11.9% of gross).
```

Twenty-five separate trades crossed the tape, a gross turnover of **Rs 33,04,230** in RELIANCE. If each had to settle on its own, that is twenty-five deliveries and twenty-five cash transfers to reconcile. After netting, all of it collapses to a single line: be a net seller of **300 shares** and **receive Rs 3,94,010**. That one settlement is just **11.9%** of the gross flow. The other 88% never needs to move at all - it was offsetting activity that cancels out.
That compression is not a convenience, it is what makes a high-volume market physically possible. The depositories and banks only ever have to move the _net_ , so the plumbing handles a fraction of the notional that actually traded. It is also why your broker can let you trade many times your settled cash intraday: nothing settles until the day's positions are netted, so only the residual ever needs funding.
Matched trades thousands of legs Clearing corp novation: becomes CCP Netting one net obligation T+1 settlement pay-in / pay-out if a member defaults, the waterfall absorbs it 1. Defaulter's own margin 2. Settlement Guarantee Fund 3. Clearing corp capital (skin) 4. Mutualised member funds used first last resort Match to novation to netting to T+1 - with the default waterfall standing guard underneath
## The T+1 clock, and optional T+0
Netting tells you _what_ settles. The cycle tells you _when_. India runs equities on **T+1** : the net obligations struck on trade day T are settled the next trading day, when the clearing corp runs **pay-in** (pulling cash and shares from those who owe) and **pay-out** (delivering to those owed). India reached full T+1 in January 2023, ahead of most of the world, then went further and launched an **optional T+0** - same-day settlement - for a growing pilot set of stocks.
The word _trading_ in "next trading day" is doing heavy lifting, and it is the part beginners get wrong:
EX 2The settlement clock with real datesNSEch07/02_settlement_timeline.py
Copy
```
# The settlement clock: a real-dated T+1 cycle versus the optional same-day T+0.
import os
from datetime import date
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

# Anchor on a real Friday so the weekend stretches T+1 to the next Monday.
trade_day = np.datetime64("2026-06-26")          # Friday 26 Jun 2026
t1 = np.busday_offset(trade_day, 1, roll="forward")  # next business day
fmt = lambda d: date.fromisoformat(str(d)).strftime("%a %d %b")

# A real price tag for the obligation that settles on T+1.
px = float(client.history(symbol="RELIANCE", exchange="NSE", interval="D",
                          start_date="2026-06-20", end_date="2026-06-26")["close"].iloc[-1])

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(10, 4.2))
x0, x1 = 0, (np.datetime64(t1) - trade_day).astype(int)   # day offsets

# Standard rolling T+1 lane.
ax.hlines(1, x0, x1, color="#7c83ff", lw=3, zorder=1)
ax.scatter([x0, x1], [1, 1], s=120, color="#7c83ff", zorder=2)
ax.annotate("T  trade matched + novated\nmargin blocked upfront", (x0, 1),
            xytext=(x0, 1.28), ha="center", fontsize=9, color="#333")
ax.annotate(f"T+1  pay-in / pay-out\ndemat + funds settle\nRs {px:,.0f}/sh", (x1, 1),
            xytext=(x1, 1.28), ha="center", fontsize=9, color="#333")

# Optional same-day T+0 lane.
ax.hlines(0.4, x0, x0, color="#16a34a", lw=3)
ax.scatter([x0], [0.4], s=120, color="#16a34a", zorder=2)
ax.annotate("T+0  optional same-day\nsettlement (pilot set)", (x0, 0.4),
            xytext=(x0, 0.10), ha="center", fontsize=9, color="#16a34a")

ax.set_xticks([x0, x1])
ax.set_xticklabels([f"{fmt(trade_day)}\n(T)", f"{fmt(t1)}\n(T+1)"])
ax.set_yticks([0.4, 1]); ax.set_yticklabels(["T+0 path", "T+1 path"])
ax.set_ylim(-0.1, 1.65); ax.set_xlim(-0.4, x1 + 0.4)
ax.set_title("Indian equity settlement clock - a Friday trade settles the next Monday")
ax.grid(axis="y", visible=False)

out = Path(__file__).with_suffix(".png")
plt.savefig(out, dpi=110, bbox_inches="tight")
print(f"Trade {fmt(trade_day)} settles {fmt(t1)} under T+1 "
      f"({x1} calendar days later over the weekend); T+0 would settle same day. Saved {out.name}")
```

Live output

```
Trade Fri 26 Jun settles Mon 29 Jun under T+1 (3 calendar days later over the weekend); T+0 would settle same day. Saved 02_settlement_timeline.png
```

![The settlement clock with real dates chart](https://openalgo.in/quant/charts/ch07_02_settlement_timeline.png)
A trade on Friday 26 June 2026 does not settle on Saturday. T+1 counts _exchange business days_ , so it settles on **Monday 29 June** - three calendar days and a full weekend after the trade, with a RELIANCE obligation of about **Rs 1,318 a share** sitting unsettled the whole time. A T+0 trade in an eligible stock, by contrast, would settle that same Friday and free the capital instantly.
Note
T+1 and the T+0 pilot are set by SEBI and the exchanges, and the eligible-stock list and exact timings change. Always check the current settlement circular rather than hard-coding a cycle. What is structural and durable is the _shape_ : faster settlement frees capital sooner and shrinks the window during which an obligation is open.
## The default waterfall: what happens when someone cannot pay
Concentrating all counterparty risk into the CCP only works if the CCP genuinely cannot fail. It is protected by a layered structure called the **default waterfall** , the side stack in the figure above. If a clearing member defaults on their pay-in, losses are absorbed in a strict order:
  * **The defaulter's own margin** - the upfront margin and collateral that member posted is seized first.
  * **The Settlement Guarantee Fund (SGF)** - a dedicated, pre-funded buffer the clearing corp maintains specifically to honour trades when a member fails.
  * **The clearing corporation's own capital** - the CCP's "skin in the game", so it shares the pain before mutualising it.
  * **Mutualised member contributions** - only as a last resort do the _non-defaulting_ members' pooled funds get touched.


This ordering is the whole point. Your trade is guaranteed not by goodwill but by a cascade of pre-funded buffers, with the person who caused the loss paying first and the broad membership paying last, if ever. It is why the guarantee in Chapter 6 is credible.
Tip
The default waterfall is also why margins are non-negotiable and collected upfront. Your posted margin is not a fee, it is the first brick in the wall that protects everyone else. When you model the cost of capital tied up as margin, remember you are funding the very guarantee you rely on.
## Why a quant actually cares
This is not trivia. Settlement mechanics feed straight into strategy economics:
  * **Carry and funding.** Between T and settlement, an obligation is open and capital is committed. A shorter cycle frees cash sooner to redeploy, and the funding cost of an unsettled position is a real input to any carry or basis trade we build in Module F.
  * **Corporate actions.** Whether you are the holder of record for a dividend, bonus or split depends on settling before the **record date**. Get the settlement timing wrong and your backtest will book a payout you never actually received - a classic, silent corporate-action bug.
  * **Short delivery.** If you sell shares for delivery and fail to deliver, the clearing corp runs an **auction** to buy them in, and the cost is charged to you and can be punishing. A market-neutral or pairs book that shorts the cash segment lives and dies by understanding this. We will return to it in Chapter 28 on short selling and SLB.
  * **Settlement risk as a position attribute.** A square-off-by-close position and a settled delivery holding carry different funding, different overnight risk and different corporate-action exposure. Treat them as different instruments, as we flagged in Chapter 6.


Heads up
Most backtests quietly assume instant, costless, guaranteed settlement. Reality has a cycle, a funding cost, corporate-action record dates and a real auction penalty for failing to deliver. Bake the settlement calendar into any strategy that holds overnight, or your paper P&L will diverge from your bank balance in ways that are hard to debug later.
We have now traced a trade from your click all the way through novation, netting, the T+1 clock and the waterfall that guarantees it. That completes the structural picture of _how the Indian market works_. With the arena mapped, Module B turns to the mathematics a quant uses to model it - starting with the humble return and the stubborn, fat-tailed personality that breaks classical finance.
On this page
