Chapters
Module F · Derivatives, Volatility & Arbitrage - Chapter 52
# The Greeks: Delta, Gamma, Vega, Theta and Rho
How an option breathes - the Greeks that measure its sensitivity to price, volatility and time, computed live on real Nifty options.
NFOINDEX
What you'll learn
  * ·Delta and gamma
  * ·Vega and theta
  * ·Rho and dividends
  * ·Greeks across strikes
  * ·Position Greeks
  * ·OpenAlgo Greeks on a Nifty option


Last chapter Black-76 handed us a fair price and four sensitivities. That was the introduction. Now we make the Greeks precise, because a working options quant does not think in _prices_ at all - she thinks in **Greeks**. A price is a single point. The Greeks are the _gradient_ : they tell you, before the market even moves, exactly how this position will gain or lose when the forward shifts, when fear rises, when the clock ticks, and when rates wander. Master the five, learn how they morph across strikes, and learn to add them up across a book, and you can hold a hundred-leg position in your head as a handful of numbers.
## Five sensitivities, one option
Every Greek is just a partial derivative of the Black-76 value with respect to one input, everything else held still. Here they are on a real, near-the-money Nifty option, with the matching put beside it:
EX 1Real Greeks for an ATM Nifty call and putNFOINDEXch52/01_position_greeks.py
Copy
```
# Real Black-76 Greeks for an ATM Nifty call and put, then the net Greeks of a position.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

LOT = 65  # NIFTY lot size


def greeks(symbol):
    # OpenAlgo computes Greeks with Black-76, priced off the synthetic-future FORWARD.
    r = client.optiongreeks(symbol=symbol, exchange="NFO", interest_rate=0.0,
                            underlying_symbol="NIFTY", underlying_exchange="NSE_INDEX")
    return r, r["greeks"]


c, ck = greeks("NIFTY28JUL2624200CE")
p, pk = greeks("NIFTY28JUL2624200PE")
fwd = c["spot_price"]

print(f"NIFTY 28-Jul-2026 options   forward (synthetic future) = {fwd:.2f}\n")
hdr = f"{'leg':<16}{'price':>8}{'IV%':>7}{'delta':>9}{'gamma':>11}{'vega':>9}{'theta':>9}{'rho':>9}"
print(hdr)
for name, q, k in [("ATM 24200 Call", c, ck), ("ATM 24200 Put", p, pk)]:
    print(f"{name:<16}{q['option_price']:>8.2f}{q['implied_volatility']:>7.2f}"
          f"{k['delta']:>+9.3f}{k['gamma']:>11.6f}{k['vega']:>+9.2f}{k['theta']:>+9.2f}{k['rho']:>+9.3f}")

# Position Greeks: SHORT 1 ATM straddle (sell the call and sell the put), one lot each.
n_delta = -(ck["delta"] + pk["delta"])
n_gamma = -(ck["gamma"] + pk["gamma"])
n_vega = -(ck["vega"] + pk["vega"])
n_theta = -(ck["theta"] + pk["theta"])  # short options -> positive theta (collect decay)

print("\nPosition Greeks - short 1 ATM straddle (sell call + sell put):")
print(f"  net delta  {n_delta:+.3f}      delta-neutral at inception")
print(f"  net gamma  {n_gamma:+.6f}   short gamma - any large move hurts")
print(f"  net vega   {n_vega:+.2f}      short vega - profits if IV falls")
print(f"  net theta  {n_theta:+.2f} pts/day = Rs {n_theta * LOT:,.1f}/day collected (x lot {LOT})")

print(f"\nShort ATM straddle: delta-neutral, short gamma and vega, banks "
      f"Rs {n_theta * LOT:,.1f}/day of theta - the trade is short volatility.")
```

Live output

```
NIFTY 28-Jul-2026 options   forward (synthetic future) = 24180.70

leg                price    IV%    delta      gamma     vega    theta      rho
ATM 24200 Call    342.95  12.72   +0.499   0.000452   +27.70    -5.85   -0.283
ATM 24200 Put     361.75  12.70   -0.501   0.000452   +27.70    -5.85   -0.298

Position Greeks - short 1 ATM straddle (sell call + sell put):
  net delta  +0.003      delta-neutral at inception
  net gamma  -0.000904   short gamma - any large move hurts
  net vega   -55.40      short vega - profits if IV falls
  net theta  +11.70 pts/day = Rs 760.6/day collected (x lot 65)

Short ATM straddle: delta-neutral, short gamma and vega, banks Rs 760.6/day of theta - the trade is short volatility.
```

The forward (the synthetic future from Chapter 49) sits at **24180.70** , so the 24200 strike is as close to the money as the chain allows. Read the five numbers off the call:
  * **Delta** (`+0.499`) is the first derivative of value with respect to the forward, `dV/dF`. The call gains about half a point for every point the forward rises. Delta is also a _hedge ratio_ : to neutralise this call you short 0.499 forwards. And it doubles as a rough risk-neutral probability that the option finishes in the money, which is why an at-the-money option sits near 0.5.
  * **Gamma** (`0.000452`) is the second derivative, `d2V/dF2`: the rate at which delta _itself_ changes as the forward moves. Delta is not a constant; gamma is its speedometer. Long options always have positive gamma.
  * **Vega** (`+27.70`) is `dV/dsigma`: the option gains about 27.70 rupees for every one percentage point rise in implied volatility. This is your exposure to _fear_ , and it is large for a thirty-day option.
  * **Theta** (`-5.85`) is `dV/dt`: the value bled per day from time passing. The buyer pays this rent; at lot 65 that is about 380 rupees a day leaking out of one ATM call.
  * **Rho** (`-0.283`) is `dV/dr`, sensitivity to the interest rate. In Black-76 off the forward it is small and, for a thirty-day Indian option where rates barely twitch, the least-watched Greek of the five.


Notice the put. Its delta is `-0.501` (a put gains when the forward falls), but its **gamma and vega are identical** to the call's, `0.000452` and `27.70`. That is no coincidence: gamma and vega depend on the _distance_ to the strike, not on which way the option points. Put-call parity guarantees a call and put at the same strike share them.
Key idea
Delta answers "which way and how much", gamma answers "how fast does delta change", vega answers "what if volatility moves", theta answers "what does waiting cost", rho answers "what if rates move". Four of the five are read straight off Black-76; only volatility must be implied back out of the market price.
## Delta is a slope, gamma is its bend
The cleanest way to _see_ delta and gamma is on the option's value curve. Plot the option's worth against the forward price and you get a smooth, upward-bending line that hugs the kinked expiry payoff from above. At any point on that curve, the **tangent's slope is delta** and the **curve's bend is gamma**.
forward price option value strike (ATM) payoff at expiry value before expiry tangent slope = delta curvature = gamma Delta is the slope of the value curve; gamma is how sharply it bends. Both live where the curve is most curved: at the money.
Deep in the money the curve runs almost parallel to the expiry payoff: slope near 1, almost no bend, so delta is near 1 and gamma is tiny. Deep out of the money the curve is nearly flat: slope near 0, bend near 0. The bend is sharpest right at the strike, which is the whole reason at-the-money options feel so alive: their delta flips fastest when the market moves.
## How the Greeks vary across strikes
That intuition becomes a picture when you sweep the whole chain. Here delta and gamma are plotted across the 28-Jul-2026 Nifty calls, from deep in the money to far out:
EX 2Delta and gamma across the strike chainNFOINDEXch52/02_greeks_across_strikes.py
Copy
```
# Delta and gamma across the Nifty call chain - delta sweeps 0 to 1, gamma peaks at the money.
import os
import time
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

# Walk the 28-Jul-2026 chain strike by strike via optiongreeks (Black-76 off the forward).
def fetch(strike):
    for _ in range(4):  # the Greeks endpoint rate-limits rapid calls; pace and retry
        r = client.optiongreeks(symbol=f"NIFTY28JUL26{strike}CE", exchange="NFO", interest_rate=0.0,
                                underlying_symbol="NIFTY", underlying_exchange="NSE_INDEX")
        if (r.get("greeks") or {}).get("delta") is not None:
            return r
        time.sleep(1.0)
    return r


rows, forward = [], None
for strike in range(22800, 25801, 200):
    r = fetch(strike)
    g = r.get("greeks") or {}
    if g.get("delta") is not None:
        forward = r["spot_price"]
        rows.append({"strike": strike, "delta": g["delta"], "gamma": g["gamma"]})
    time.sleep(0.8)

df = pd.DataFrame(rows)

sns.set_theme(style="whitegrid")
fig, ax1 = plt.subplots(figsize=(8, 4.5))
ax1.plot(df["strike"], df["delta"], color="#7c83ff", lw=2, marker="o", ms=4, label="Delta (call)")
ax1.axvline(forward, color="#dc2626", ls="--", lw=1.2, label=f"forward {forward:.0f}")
ax1.set_xlabel("Strike")
ax1.set_ylabel("Delta", color="#7c83ff")
ax1.set_ylim(0, 1)

ax2 = ax1.twinx()
ax2.plot(df["strike"], df["gamma"], color="#16a34a", lw=1.8, marker="s", ms=3, label="Gamma")
ax2.set_ylabel("Gamma", color="#16a34a")
ax2.grid(False)

ax1.set_title("Nifty 28-Jul-2026 call Greeks across strikes - delta S-curve, gamma peaks ATM")
ax1.legend(loc="center left")
out = Path(__file__).with_suffix(".png")
plt.savefig(out, dpi=110, bbox_inches="tight")

peak = df.loc[df["gamma"].idxmax(), "strike"]
print(f"Delta {df['delta'].max():.2f} (ITM) -> {df['delta'].min():.2f} (OTM); "
      f"gamma peaks at strike {peak:.0f} near forward {forward:.0f}. Saved {out.name}")
```

Live output

```
Delta 0.92 (ITM) -> 0.04 (OTM); gamma peaks at strike 24200 near forward 24181. Saved 02_greeks_across_strikes.png
```

![Delta and gamma across the strike chain chart](https://openalgo.in/quant/charts/ch52_02_greeks_across_strikes.png)
Delta traces the famous **S-curve** : it runs from **0.92** at the deep-in-the-money 22800 strike, glides through about 0.5 at the forward, and tails to **0.04** at the far 25800 strike. Gamma, the green line, is a hump that **peaks at 24200** , right on top of the forward, and decays symmetrically on both wings. Vega and theta share that same single-peaked, at-the-money-maximal shape (you can confirm it by swapping the plotted column in the script). The lesson is structural: _all the second-order action concentrates at the money_. An at-the-money option is where you get the most gamma, the most vega and the most theta per rupee of premium, and the in- and out-of-the-money wings are progressively more inert.
Tip
This is why traders pick strikes by Greek, not by price. Want pure directional exposure with little time decay? Buy a deep-in-the-money option (delta near 1, gamma and theta small) - it behaves almost like the future. Want maximum convexity into an event? Buy at the money, where gamma and vega peak. The strike is a dial on which Greek you are buying.
## Position Greeks: a book is just a sum
The reason quants think in Greeks rather than prices is that **Greeks add**. The delta of a portfolio is the signed sum of each leg's delta times its quantity; the same holds for gamma, vega and theta. A messy multi-leg book collapses to five numbers. The example computes this for a classic structure, a **short at-the-money straddle** (sell the 24200 call and sell the 24200 put):
  * **net delta`+0.003`** - the opposing call and put deltas cancel, so the position is _delta-neutral_ at inception. It does not care, to first order, which way Nifty moves.
  * **net gamma`-0.000904`** - short two long-gamma options means negative gamma. A big move in either direction hurts, because delta runs against you.
  * **net vega`-55.40`** - short vega. If implied volatility _falls_ , the position profits; if fear spikes, it loses about 55 rupees per vol point per unit.
  * **net theta`+11.70` points a day**, which at lot 65 is about **760.6 rupees a day** collected. The seller banks the rent the buyers pay.


That single line - delta-neutral, short gamma, short vega, positive theta - _is_ the trade. It is a bet that realised volatility comes in below the implied volatility priced into those options. You are paid 760 rupees a day to carry the risk that a large move blows through your short gamma.
Heads up
Positive theta is never free. The short straddle's `+760.6` rupees a day is the premium for being _short gamma_ : a single gap of a few hundred Nifty points can erase weeks of collected theta in one session, because your losses accelerate as the move grows. Gamma and theta sit on opposite ends of the same seesaw, and that seesaw tilts violently into expiry, when gamma explodes for at-the-money options. Short-gamma books demand hard stops and position limits, not hope.
## The signs that define a strategy
Strip away the structure names and every options position reduces to the _signs_ of its Greeks. Long gamma with negative theta means you have bought convexity and you pay for it daily; you want movement. Short gamma with positive theta means you have sold convexity and you collect daily; you want stillness. Long vega wants implied volatility to rise; short vega wants it to fall. Delta is the part you can hedge away with the future whenever you choose, leaving the _pure volatility_ bet underneath. That is the deepest idea in this chapter: once you delta-hedge, an option stops being a directional instrument and becomes a clean trade on gamma, theta and vega - on volatility itself.
Note
Rho is the runt for Indian equity options. Over a thirty-day life the policy rate is effectively fixed, so the `-0.283` rho barely moves the position. It matters for long-dated options and for currency and rate derivatives, where the interest-rate leg is the whole point. Note the unit conventions the engine uses: theta is per calendar day, vega and rho are per one percentage point of their input. Always check units before you trust a Greek.
These five numbers, summed across a book and watched in real time, are how a derivatives desk actually holds risk. But notice the input we kept quietly fixing: the implied volatility, 12.7 percent at the money here, was different at every strike in the chain. That refusal of the market to quote one volatility is the volatility surface, and India's own gauge of it, India VIX, is where we go next.
On this page
