Chapters
Module D · HFT, Execution & Trading Technology - Chapter 40
# Kill Switches, Risk Controls and Algo Surveillance
The safety layer every automated trader needs - pre-trade risk checks, position and loss limits, the kill switch and the surveillance that watches for runaways.
NSE
What you'll learn
  * ·Pre-trade risk checks
  * ·Position and loss limits
  * ·The kill switch
  * ·Throttles and rate limits
  * ·Exchange-level surveillance
  * ·Designing fail-safe systems


On a single morning in 2012, a well-known US market-making firm deployed new code, an old dormant flag woke up logic that should have stayed asleep, and over about forty-five minutes its system fired millions of unintended orders into the market and lost close to 440 million dollars - more than the firm was worth. No human could read, understand and intervene at that speed. The only thing that could have stopped it was another piece of software saying _no_ faster than the strategy could say yes. That is the subject of this chapter, and it is the right note on which to close Module D. You have taught your bot to see the market, form a signal, size a trade and fire an order through a gateway. Now you teach it the one reflex that outranks every signal it will ever have: the ability to refuse its own orders.
## The pre-trade gate: the last code before the wire
A **pre-trade risk check** is a small, strict piece of code that sits between your strategy and the exchange, and that every order must pass before it leaves your process. It does not care how confident the signal feels or how clever the model is. It knows only your limits, and it can veto. The design principle from Chapter 29 - keep the stages separate, let the risk layer be the last word - becomes concrete here: the gate is deliberately dumb, independent of the signal, and easy to reason about, because it is the thing standing between a bug and a blown account.
Think of it as a short stack of gates in series. An order intent arrives and must clear a **position** check, a **loss** check and a **rate** check, with a **kill switch** able to slam the whole stack shut. Any gate can reject. A rejected order is not silently dropped - it is logged and it raises an alert, because a flood of rejections is itself a signal that something upstream has gone wrong. Only an order that clears every gate reaches the exchange. In OpenAlgo terms the gate lives in front of the order gateway: the same place you would point at a sandbox first, then at a live account.
Order intent buy / sell qty Position exposure cap Loss daily limit Rate orders / sec Kill switch halt all Exchange order sent rejected - logged and alerted, no order leaves the process Every order earns its way to the exchange by clearing each gate; any gate can veto, and the kill switch can shut all of them at once
Key idea
A pre-trade risk gate is the last code an order passes before the wire. It is intentionally simple, independent of the signal, and has the power of veto. The signal proposes; the gate disposes. Build it as a separate, testable layer so that when a strategy misbehaves - and one day it will - the gate, not your account, absorbs the mistake.
## Position and loss limits
Two limits do most of the work. A **position limit** caps how much exposure you may hold, expressed not as a share count but as rupee value, because a thousand shares means something very different in a Rs 100 stock than in a Rs 4,000 one. You compute the projected position value from a real quote and reject anything that pushes you past the cap. A **loss limit** caps how much you may lose in a day; once cumulative profit and loss falls through it, no new risk-increasing order is allowed.
The first example builds exactly this gate. It pulls a live RELIANCE quote for sizing - the last traded price came back at Rs 1318.10 - and applies a policy of at most Rs 20,00,000 of exposure, a Rs 25,000 daily loss limit and a throttle of four orders per ten seconds. It then walks eight proposed orders through the gate:
EX 1A pre-trade risk gate sizing off a live quoteNSEch40/01_pretrade_gate.py
Copy
```
# Pre-trade risk gate: check proposed orders against position, loss and rate limits.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# --- REAL quote drives sizing: position VALUE = shares * live LTP ---
q = client.quotes(symbol="RELIANCE", exchange="NSE")["data"]
ltp = q["ltp"]

# --- risk policy (the numbers a desk would set up front) ---
MAX_POSITION_VALUE = 20_00_000   # rupees of gross exposure allowed in this symbol
DAILY_LOSS_LIMIT = 25_000        # rupees; breaching this trips the kill switch
RATE_LIMIT_N = 4                 # at most N accepted orders ...
RATE_WINDOW_S = 10               # ... per rolling window of this many seconds


class RiskGate:
    def __init__(self, ltp):
        self.ltp = ltp
        self.position = 0          # net shares currently held
        self.sent = []             # timestamps (s) of orders the gate accepted
        self.killed = False        # latches True once the loss switch trips

    def check(self, side, qty, now, day_pnl):
        sign = 1 if side == "BUY" else -1
        new_pos = self.position + sign * qty
        # GATE 1 - loss / kill switch (checked first, and it latches)
        if self.killed or day_pnl <= -DAILY_LOSS_LIMIT:
            self.killed = True
            return False, "kill switch - daily loss limit"
        # GATE 2 - position cap, sized off the REAL ltp
        value = abs(new_pos) * self.ltp
        if value > MAX_POSITION_VALUE:
            return False, f"position cap (Rs {value:,.0f})"
        # GATE 3 - rate / throttle limit
        recent = [t for t in self.sent if now - t < RATE_WINDOW_S]
        if len(recent) >= RATE_LIMIT_N:
            return False, f"rate limit ({RATE_LIMIT_N}/{RATE_WINDOW_S}s)"
        self.position = new_pos     # all gates passed - commit the order
        self.sent.append(now)
        return True, f"accepted, pos -> {new_pos}"


# proposed orders walking through a session: (t_seconds, side, qty, running_day_pnl)
tests = [
    (0,  "BUY",  500,    0),
    (1,  "BUY",  500,  2000),
    (2,  "BUY",  600,  1500),   # would push exposure over the position cap
    (3,  "BUY",  400,  -500),
    (4,  "BUY",  100,  -300),
    (5,  "SELL", 200,  -200),   # 5th order inside 10s -> throttled
    (18, "BUY",  200, -26000),  # day P&L now below the loss limit -> kill
    (20, "BUY",  100, -26000),  # switch has latched, stays blocked
]

gate = RiskGate(ltp)
print(f"RELIANCE LTP Rs {ltp:.2f} | caps: exposure <= Rs {MAX_POSITION_VALUE:,}, "
      f"loss <= Rs {DAILY_LOSS_LIMIT:,}, rate <= {RATE_LIMIT_N}/{RATE_WINDOW_S}s\n")
print(" t  order      day_pnl   result   reason")
passed = 0
for t, side, qty, pnl in tests:
    ok, why = gate.check(side, qty, t, pnl)
    passed += ok
    print(f"{t:2d}  {side:4s} {qty:4d}  {pnl:8d}   {'PASS ' if ok else 'BLOCK'}   {why}")

print(f"\n{passed} of {len(tests)} proposed orders passed the gate; final position "
      f"{gate.position} shares; kill switch {'TRIPPED' if gate.killed else 'armed'}.")
```

Live output

```
RELIANCE LTP Rs 1318.10 | caps: exposure <= Rs 2,000,000, loss <= Rs 25,000, rate <= 4/10s

 t  order      day_pnl   result   reason
 0  BUY   500         0   PASS    accepted, pos -> 500
 1  BUY   500      2000   PASS    accepted, pos -> 1000
 2  BUY   600      1500   BLOCK   position cap (Rs 2,108,960)
 3  BUY   400      -500   PASS    accepted, pos -> 1400
 4  BUY   100      -300   PASS    accepted, pos -> 1500
 5  SELL  200      -200   BLOCK   rate limit (4/10s)
18  BUY   200    -26000   BLOCK   kill switch - daily loss limit
20  BUY   100    -26000   BLOCK   kill switch - daily loss limit

4 of 8 proposed orders passed the gate; final position 1500 shares; kill switch TRIPPED.
```

Four of the eight orders passed. The third was a buy of 600 shares that would have lifted the holding to 1,600 shares, worth Rs 21,08,960 against the live price - over the Rs 20,00,000 cap, so the gate rejected it before it could ever reach the exchange. Notice that the gate did not block trading outright; the next two smaller orders, which kept exposure under the cap, sailed through to a position of 1,500 shares. A good position limit shapes behaviour rather than freezing it.
Tip
Express position limits in currency, not share count, and size them off the live price every time. A 1,000-share limit silently becomes a different risk as the stock moves, but a Rs 20 lakh exposure cap means the same thing on every day and across every instrument. The same logic underlies the exchange's own SPAN and exposure margins from Chapter 58 - risk is measured in money.
## The kill switch: one switch, latched
Limits clip individual orders. The **kill switch** is the blunt instrument that stops everything: it cancels working orders, blocks new ones, and optionally flattens open positions. The single most important property of a real kill switch is that it **latches**. Once tripped, it stays tripped until a human deliberately resets it. A switch that re-arms itself the moment profit and loss ticks back above the limit is not a safety device - it is a trapdoor that keeps reopening under the same falling weight.
In the example, the daily loss limit and the kill switch are the same gate, and it is checked first. When the running profit and loss reached Rs -26,000, past the Rs -25,000 limit, the switch tripped and the order was blocked. Two seconds later, with profit and loss unchanged, a smaller order was blocked again for the same reason, because the switch had latched. Exchanges in India require trading members to maintain kill-switch functionality precisely so that a runaway algo can be cut off at the source, and your own application should carry one too, independent of the broker's.
Heads up
A kill switch that automatically re-arms is worse than none, because it lulls you into trusting it. Make the trip one-way: latch it, log who and what tripped it, and require a manual, deliberate reset. The few minutes of friction in restarting a halted strategy are the whole point - they force a human to look before the machine trades again.
## Throttles, rate limits and surveillance
Even when every order is individually within limits, their _rate_ can be the hazard. A **throttle** or rate limit caps how many orders you may send in a window - in the example, four per ten seconds. The fifth order inside that window, a sell of 200 shares, was rejected by the rate gate even though it broke no position or loss limit. Rate limits are your defence against the duplicated-order runaway from Chapter 29: a retry storm or a loop firing every tick instead of on a state change.
This matters beyond your own books because exchanges watch it. The **order-to-trade ratio** from Chapter 35 - how many orders you place for each one that actually trades - is monitored and penalised when it runs hot, which is the exchange's way of policing quote stuffing and excessive messaging. Layered on top is **market surveillance** : automated systems that flag spoofing, layering and manipulative patterns across all participants. The retail algo framework from Chapter 39, set out in the SEBI circular of 4 February 2025, pushes the same discipline down to retail by requiring brokers to run risk controls on API-driven order flow. Your internal throttle is not just self-protection; it keeps you on the right side of all of this.
Note
Rate limits, the order-to-trade ratio and exchange surveillance are three views of one idea: the system cares not only about each order but about the pattern of orders. A clean pattern - measured, mostly-filled, within throttle - keeps you compliant and cheap. A messy one invites penalties and scrutiny even if no single order broke a rule.
## Designing fail-safe systems
The gates above are necessary but not sufficient; the architecture around them has to fail safely. **Fail closed** , not open: if the risk module cannot evaluate an order - a missing quote, an unreachable limit store - the safe default is to reject, never to wave it through. Add a **dead-man switch** , a heartbeat the strategy must keep sending; if it goes silent, assume the worst and flatten. Make every order **idempotent** and reconcile against the broker's order book, so a crash and restart cannot double a position. And test the failure paths, because the gate that has never been tripped in anger is the one that fails when you finally need it.
The second example shows why all of this earns its keep. It anchors a simulation to the real volatility of RELIANCE five-minute bars, then lets a runaway strategy pile on exposure every bar - the classic re-adding bug - with a slight negative edge:
EX 2A daily-loss kill switch capping a runaway strategyNSEch40/02_killswitch_pnl.py
Copy
```
# A runaway strategy hitting a daily-loss kill switch: managed P&L flatlines once it trips.
import os
from datetime import datetime, timedelta
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

# --- anchor the simulation to REAL per-bar volatility of a liquid name ---
end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d")
df = client.history(symbol="RELIANCE", exchange="NSE", interval="5m",
                    start_date=start, end_date=end)
sigma = df["close"].pct_change().dropna().std()   # real 5m return std

# --- the runaway: a bug re-adds to a losing book every bar (position keeps growing) ---
rng = np.random.default_rng(42)
N = 75                                  # one 5m session
DAILY_LOSS_LIMIT = 50_000               # rupees; the kill-switch trip level
ADD_PER_BAR = 5_00_000                  # notional piled on each bar (the runaway)
DRIFT = -0.0004                         # adverse per-bar drift: a negative-edge strategy

notional = ADD_PER_BAR * np.arange(1, N + 1)            # exposure grows each bar
ret = rng.normal(DRIFT, sigma, N)                       # per-bar market move
bar_pnl = notional * ret                                # rupees made/lost per bar
unmanaged = np.cumsum(bar_pnl)                          # no risk control at all

# --- the kill switch: first time cumulative loss breaches the limit, flatten and freeze ---
managed = unmanaged.copy()
trip = np.argmax(unmanaged <= -DAILY_LOSS_LIMIT) if (unmanaged <= -DAILY_LOSS_LIMIT).any() else -1
if trip >= 0:
    managed[trip:] = unmanaged[trip]                    # P&L flatlines from the trip bar on

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(11, 5))
t = np.arange(N)
ax.plot(t, unmanaged, color="#dc2626", lw=1.6, label="no kill switch (runaway)")
ax.plot(t, managed, color="#7c83ff", lw=1.8, label="kill switch active")
ax.axhline(-DAILY_LOSS_LIMIT, color="#16a34a", ls="--", lw=1.2,
           label=f"loss limit Rs {DAILY_LOSS_LIMIT:,}")
if trip >= 0:
    ax.scatter([trip], [managed[trip]], color="#7c83ff", s=80, zorder=5)
    ax.annotate("switch trips - book flattened", (trip, managed[trip]),
                textcoords="offset points", xytext=(12, 14), fontsize=10, color="#7c83ff")
ax.set_title("Daily-loss kill switch caps a runaway strategy (RELIANCE 5m vol)", fontsize=13)
ax.set_xlabel("5-minute bars into the session")
ax.set_ylabel("cumulative P&L (Rs)")
ax.legend(loc="lower left", framealpha=0.9)
fig.tight_layout()
out = Path(__file__).with_suffix(".png")
plt.savefig(out, dpi=110, bbox_inches="tight")

print(f"sigma {sigma*100:.3f}%/bar; switch trips at bar {trip}; managed P&L frozen at "
      f"Rs {managed[-1]:,.0f} vs runaway Rs {unmanaged[-1]:,.0f}. Saved {out.name}")
```

Live output

```
sigma 0.132%/bar; switch trips at bar 21; managed P&L frozen at Rs -56,468 vs runaway Rs -567,349. Saved 02_killswitch_pnl.png
```

![A daily-loss kill switch capping a runaway strategy chart](https://openalgo.in/quant/charts/ch40_02_killswitch_pnl.png)
With no control, the runaway loses Rs 5,67,349 over the session and is still accelerating at the close. With a Rs 50,000 daily-loss kill switch, the switch trips at bar 21 and the managed profit and loss freezes at Rs -56,468 - a single bad bar overshot the limit before the switch caught it, an honest reminder that a kill switch caps the bleeding near the limit but cannot perfectly pin it. Even so, the controlled loss is roughly a tenth of the uncontrolled one. That gap is the entire value of the risk layer, and it is why no automated strategy should ever run without one.
This closes Module D. You can now build the full loop - see, decide, size, route, and refuse - which is the complete anatomy of an execution system. Module E turns from the plumbing to the prediction: the time-series models, from volatility estimation to cointegration, that try to give the loop something genuinely worth trading.
On this page
