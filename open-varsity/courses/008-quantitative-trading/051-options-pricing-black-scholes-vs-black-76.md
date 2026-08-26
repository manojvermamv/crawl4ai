Chapters
Module F · Derivatives, Volatility & Arbitrage - Chapter 51
# Options Pricing: Black-Scholes vs Black-76
Why Indian F&O is priced with Black-76 off the synthetic future, not Black-Scholes off spot - the models, their assumptions and where they break.
NFOINDEX
What you'll learn
  * ·Put-call parity
  * ·The synthetic future
  * ·Black-Scholes assumptions
  * ·Black-76 off the forward
  * ·Why India uses Black-76
  * ·Pricing a Nifty option


An option's price is one of the strangest numbers in finance: it is the price of _uncertainty itself_. A model that turns a forward price, a strike, some time, and a volatility into that fair value is the crown jewel of derivatives theory. You have heard of Black-Scholes. But for Indian markets the right tool is its close cousin, **Black-76** , and the difference is not academic: feed a pricer the wrong underlying and every number it produces is quietly corrupted. This chapter is about getting the _price_ right. The sensitivities that fall out of the same model - the Greeks - get their own dedicated chapter next.
## Put-call parity and the synthetic future
Before any model, there is one relationship that holds with _no assumptions at all_ , enforced by arbitrage alone: **put-call parity**. For European options at the same strike and expiry,
`C - P = e^(-rT) (F - K)`
where C and P are the call and put prices, K the strike, F the forward, r the rate and T the time to expiry. Rearranged, it says something remarkable: a long call plus a short put at the same strike has exactly the payoff of a _long forward_ struck at K. That bundle is a **synthetic future**. You never need a pricing model to see it; it is pure cash-and-carry logic (Chapter 49).
Turn the equation around and parity hands you the forward the market is actually using:
`F = K + e^(rT) (C - P)`
Pick the strike nearest the money, read the call and put prices off the chain, and out pops the **synthetic future** - the forward implied by the options themselves. This is the number you feed the pricer, and it is exactly what OpenAlgo's Greeks engine does under the hood. In the example below the printed forward, 24058.30, was recovered this way, not taken from spot.
Note
Put-call parity is **model-free**. It assumes nothing about how prices move - not normal returns, not constant volatility, none of what Black-Scholes needs - only that you cannot make riskless money. So the synthetic forward it gives you is more trustworthy than any spot-plus-carry forward you would otherwise guess, because it already contains the market's real view of dividends and funding.
## Black-Scholes off spot, Black-76 off the forward
Here is the distinction most courses skip. **Black-Scholes** prices an option off the **spot** price of the underlying and carries it forward at an interest rate. **Black-76** (Fischer Black, 1976) prices directly off the **forward**. They share the same lognormal DNA; only the underlying differs. The call in Black-76 form is
`C = e^(-rT) [ F N(d1) - K N(d2) ]`
with `d1 = [ ln(F/K) + (sigma^2 / 2) T ] / (sigma sqrt(T))` and `d2 = d1 - sigma sqrt(T)`, where N is the standard normal CDF. The put is the mirror image. Notice the rate appears only as a discount factor out front; all the carry is already baked into F.
Both models lean on the same idealisations: returns are **lognormal** , volatility and rates are **constant** , trading is continuous and frictionless, and exercise is European. None of these is exactly true, which we will come back to.
Why does India use Black-76? Because Indian index and stock options settle against the **futures / forward** , and that forward is sitting right there in the chain via parity. Price a Nifty option off spot with vanilla Black-Scholes and you must _guess_ the cost of carry and the dividend stream to rebuild the forward; get either wrong and the forward is mis-stated, and every output inherits the error. Black-76 sidesteps the guess entirely by taking the market's own forward as the input.
Black-76 inputs F forward (synthetic future) K strike T time to expiry r interest rate σ volatility (the unknown) Black-76 F N(d1) - K N(d2) discounted to today Fair option price matches the market quote run backwards: solve for σ = implied volatility Black-76 turns the forward, strike, time, rate and volatility into a price - and run backwards, a market price yields implied volatility.
Key idea
For Indian F&O (NFO, BFO, MCX, CDS), use **Black-76** , pricing off the **forward** (the synthetic future), not spot. This is not pedantry: pricing an Indian index option off spot mis-states the forward by the cost of carry, and every downstream number - price, implied vol, and every Greek - inherits the error. OpenAlgo computes its Greeks with Black-76 for exactly this reason.
## Implied volatility: the model run backwards
Black-76 needs five inputs and returns a price. Four of them - forward, strike, time, rate - you read straight off the market. The fifth, **volatility** , is the one number you cannot observe, and that single fact reshapes the entire options world.
Because everything else is known, the model can be run _backwards_. Take the option's actual market price, hold the four observables fixed, and solve for the volatility that makes the formula match. That number is the **implied volatility (IV)** - the market's own forecast of how much the underlying will move, expressed in the only language options traders truly speak. In the first example the 24000 call trades at 166.75, which inverts to an IV of about 11.1 percent.
IV, not price, is the real output of the model. A 50-rupee option and a 5-rupee option cannot be compared directly, but their implied vols can. And here is the tell that drives the next two chapters: the market does not quote _one_ implied volatility - it quotes a different IV at every strike. That refusal is the **volatility surface** (Chapter 53), and India's headline gauge of it is India VIX (Chapter 54).
Tip
Treat the price as the input and the **implied volatility as the output**. Professionals quote and think in vol, because it strips out the mechanical effects of strike, spot and time and leaves the one thing genuinely in dispute: how much the market expects things to move.
## A price, and the sensitivities that come with it
Run Black-76 and you get more than a price. Because the formula is smooth in each input, you can differentiate it, and those derivatives - the **Greeks** - tell you how the price will move when the forward, volatility, time or rates change. Here they are for an at-the-money Nifty call, computed off the synthetic future:
EX 1Black-76 Greeks on a Nifty optionNFOINDEXch51/01_greeks.py
Copy
```
# Black-76 Greeks on a Nifty option - the numbers that say how it breathes.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# OpenAlgo computes Greeks with Black-76, priced off the synthetic-future FORWARD.
g = client.optiongreeks(symbol="NIFTY30JUN2624000CE", exchange="NFO", interest_rate=0.0,
                        underlying_symbol="NIFTY", underlying_exchange="NSE_INDEX")
gk = g["greeks"]

print(f"Option : {g['symbol']}   price {g['option_price']}")
print(f"Forward: {g['spot_price']:.2f}  (the synthetic future)   IV: {g['implied_volatility']}%\n")
print(f"  Delta  {gk['delta']:+.3f}   moves this much per 1 point of the forward")
print(f"  Gamma  {gk['gamma']:.5f}   how fast delta itself changes")
print(f"  Vega   {gk['vega']:+.2f}    gained per +1% in implied volatility")
print(f"  Theta  {gk['theta']:+.2f}   lost every day to time decay")
print(f"  Rho    {gk['rho']:+.3f}")
print("\nThese are Black-76 Greeks - the correct model for Indian F&O, priced off the forward (not spot).")
```

Live output

```
Option : NIFTY30JUN2624000CE   price 166.75
Forward: 24058.30  (the synthetic future)   IV: 11.14%

  Delta  +0.571   moves this much per 1 point of the forward
  Gamma  0.00115   how fast delta itself changes
  Vega   +11.99    gained per +1% in implied volatility
  Theta  -11.36   lost every day to time decay
  Rho    -0.027

These are Black-76 Greeks - the correct model for Indian F&O, priced off the forward (not spot).
```

The same machine that prints the 166.75 fair value also prints a delta of about 0.57, a vega near 12 and a theta around minus 11. These sensitivities sweep in characteristic shapes across strikes - delta, for instance, runs from near 1 deep in the money down to near 0 far out of it:
EX 2The delta curve across strikesNFOINDEXch51/02_delta_curve.py
Copy
```
# The delta curve: how an option's delta sweeps from 0 to 1 across strikes.
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

rows = []
for strike in range(23400, 24701, 100):
    r = client.optiongreeks(symbol=f"NIFTY30JUN26{strike}CE", exchange="NFO", interest_rate=0.0,
                            underlying_symbol="NIFTY", underlying_exchange="NSE_INDEX")
    g = r.get("greeks") or {}
    if g.get("delta") is not None:
        rows.append({"strike": strike, "delta": g["delta"], "gamma": g["gamma"]})
    time.sleep(0.3)

df = pd.DataFrame(rows)
forward = 24058

sns.set_theme(style="whitegrid")
fig, ax1 = plt.subplots(figsize=(8, 4.5))
ax1.plot(df["strike"], df["delta"], color="#7c83ff", lw=2, marker="o", ms=4, label="Delta (call)")
ax1.axvline(forward, color="#888", ls="--", lw=1.2, label="forward ~24058")
ax1.set_xlabel("Strike")
ax1.set_ylabel("Delta", color="#7c83ff")

ax2 = ax1.twinx()
ax2.plot(df["strike"], df["gamma"], color="#16a34a", lw=1.6, label="Gamma")
ax2.set_ylabel("Gamma", color="#16a34a")
ax2.grid(False)

ax1.set_title("Nifty call Greeks across strikes - delta S-curve, gamma peaks at the money")
ax1.legend(loc="center left")
out = Path(__file__).with_suffix(".png")
plt.savefig(out, dpi=110, bbox_inches="tight")
print(f"Delta runs {df['delta'].max():.2f} (deep ITM) -> {df['delta'].min():.2f} (far OTM). Saved {out.name}")
```

Live output

```
Delta runs 0.93 (deep ITM) -> 0.04 (far OTM). Saved 02_delta_curve.png
```

![The delta curve across strikes chart](https://openalgo.in/quant/charts/ch51_02_delta_curve.png)
We will not unpack each Greek here. The sensitivities are the entire subject of the **next chapter (Chapter 52)** , which treats delta, gamma, vega, theta and rho properly, shows how each varies across strikes, and adds them up across a multi-leg book. For now the point is narrower and structural: _price and Greeks come out of the same Black-76 engine fed the same forward_. Get the underlying wrong and you do not merely mis-price the option - you corrupt every sensitivity in one stroke. That is why the pricing choice in this chapter is the foundation everything in the next one stands on.
## Wrong, but useful
A confession the textbooks bury: Black-76 is _wrong_. It assumes constant volatility and lognormal returns, and the math module already showed markets have neither - fat tails (Chapter 11) and volatility that clusters and jumps. Real option prices bulge above the model in the tails, which is precisely why IV is not flat across strikes.
So why is a model nobody believes the foundation of a trillion-rupee industry? Because it is the common **language**. No one uses Black-76 to find the "true" value of an option; they use it as a **translator** - to convert a messy market price into one clean, comparable number, implied volatility, and to read off the sensitivities needed to hedge. The model's most famous failure, that real IV varies by strike and expiry, is not a bug to be patched but the most heavily traded signal in all of options, and it is exactly where the next few chapters go.
Heads up
Never mistake the model for the market. Black-76 is a constant-volatility model living in a fat-tailed, jumpy world, so it will mis-price deep out-of-the-money options (the wings) if you force a single volatility across them. Use it to _quote in vol and hedge_ , not to declare an option cheap or rich on price alone. The skew exists because the model is incomplete, not because the market is wrong.
## Try it yourself
  * Recover the forward yourself. Read an at-the-money call and put off the chain and compute `F = K + e^(rT) (C - P)`. Does your synthetic future match the 24058.30 the example printed?
  * Invert for IV both ways. Solve the call's price for implied vol, then do the same for the put at the same strike. Parity says the two IVs should nearly agree - do they?
  * Price an out-of-the-money call with Black-76 using the at-the-money implied vol, then compare to its real market quote. Where they diverge, you have just measured the skew - the subject of Chapter 53.


## Recap
  * **Put-call parity** (`C - P = e^(-rT) (F - K)`) is model-free and hands you the **synthetic future** , the forward the options themselves imply - the correct underlying to price against.
  * **Black-Scholes** prices off **spot** ; **Black-76** prices off the **forward**. Indian F&O settles against the forward, so Black-76 off the synthetic future is the right tool, and using spot mis-states the forward by the cost of carry.
  * The model needs **forward, strike, time, rate and volatility** ; only volatility is unobservable, so run the model backwards from the market price to get **implied volatility** , its real output.
  * Price and Greeks come from the **same engine and the same forward** ; the Greeks get their full treatment in **Chapter 52**.
  * Black-76 is **"wrong but useful"** - a constant-vol model in a fat-tailed world, used as a common language (IV) and a hedging tool, not as literal truth.


The price is settled. What remains is how that price _moves_ - how the option gains and loses as the forward shifts, as fear rises, and as the clock runs down. Those sensitivities, the Greeks, are how a real derivatives desk holds risk, and they are next.
On this page
