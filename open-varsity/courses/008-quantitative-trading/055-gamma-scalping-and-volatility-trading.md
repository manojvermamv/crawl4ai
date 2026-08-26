Chapters
Module F · Derivatives, Volatility & Arbitrage - Chapter 55
# Gamma Scalping and Volatility Trading
Volatility as an asset you can trade - delta-hedged straddles, gamma scalping, variance and the Indian expiry-day effects that drive it.
NFOINDEX
What you'll learn
  * ·Volatility as an asset
  * ·Delta-hedged options
  * ·Gamma scalping P&L
  * ·Variance and straddles
  * ·Expiry-day effects
  * ·Selling vs buying vol


Here is the idea that separates an options _trader_ from someone who merely buys calls and puts: you can trade **volatility itself** , with no view on direction at all. You can bet the market will move a lot, or barely move, and profit from being right about the _size_ of the swing regardless of which way it goes. Given what we learned in Chapter 9 - that volatility, unlike direction, is genuinely forecastable - this is the most natural quant trade in the options world. It's also where India's enormous options market truly lives. Let's finish the derivatives module by trading vol.
## Volatility as an asset
When you buy an at-the-money call _and_ an at-the-money put together - a **straddle** - you don't care which way the market goes; you only care that it _moves enough_. You've bought volatility. Sell that same pair and you've sold volatility - you now want the market to sit still. Volatility has become the thing you're trading, an asset in its own right, completely separate from direction.
## The long straddle: buying a big move
Let's price and plot a real one - a long Nifty straddle, buying both the ATM call and put:
EX 1A long straddle payoffNFOINDEXch55/02_straddle.py
Copy
```
# A long straddle buys volatility: it profits from a BIG move either way.
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

STRIKE = 24000
call = client.quotes(symbol=f"NIFTY30JUN26{STRIKE}CE", exchange="NFO")["data"]["ltp"]
put = client.quotes(symbol=f"NIFTY30JUN26{STRIKE}PE", exchange="NFO")["data"]["ltp"]
cost = call + put                                   # premium paid for the straddle

spots = np.arange(STRIKE - 1200, STRIKE + 1200, 10)
payoff = np.abs(spots - STRIKE) - cost              # long straddle P&L at expiry
lower, upper = STRIKE - cost, STRIKE + cost         # breakevens

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(spots, payoff, color="#7c83ff", lw=2)
ax.axhline(0, color="#555", lw=1)
ax.fill_between(spots, payoff, 0, where=payoff > 0, color="#16a34a", alpha=0.2)
ax.fill_between(spots, payoff, 0, where=payoff < 0, color="#dc2626", alpha=0.2)
ax.axvline(lower, color="#888", ls="--", lw=1)
ax.axvline(upper, color="#888", ls="--", lw=1)
ax.set_title(f"Long {STRIKE} straddle - cost {cost:.0f}, profits beyond {lower:.0f} / {upper:.0f}")
ax.set_xlabel("NIFTY at expiry")
ax.set_ylabel("Profit / loss")

out = Path(__file__).with_suffix(".png")
plt.savefig(out, dpi=110, bbox_inches="tight")
print(f"Straddle cost {cost:.0f} (call {call} + put {put}). Breaks even at {lower:.0f} and {upper:.0f}. Saved {out.name}")
```

Live output

```
Straddle cost 275 (call 166.75 + put 108.45). Breaks even at 23725 and 24275. Saved 02_straddle.png
```

![A long straddle payoff chart](https://openalgo.in/quant/charts/ch55_02_straddle.png)
The payoff is a clean V. You paid 275 points (call + put) for the privilege, so you _lose_ if Nifty expires near the strike - the worst case is a quiet market that wastes your premium. But break out beyond the breakevens (23725 or 24275) in _either_ direction and you profit, more the further it runs. A long straddle is a pure bet that the coming move will be **bigger** than the market has priced in. Which raises the obvious question: what _has_ the market priced in?
## The volatility risk premium
This is the deepest fact in options trading. On average, **implied volatility exceeds the volatility that actually shows up.** Compare them directly:
EX 2The volatility risk premiumINDEXch55/01_vol_risk_premium.py
Copy
```
# The volatility risk premium: implied vol usually exceeds what actually happens.
import os
from datetime import datetime, timedelta

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# Implied: what options price in (India VIX, ~30-day forward-looking).
vix = client.quotes(symbol="INDIAVIX", exchange="NSE_INDEX")["data"]["ltp"]

# Realized: what the market actually did over the last 30 sessions.
end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
r = client.history(symbol="NIFTY", exchange="NSE_INDEX", interval="D",
                   start_date=start, end_date=end)["close"].pct_change().dropna()
realized = r.tail(30).std() * (252 ** 0.5) * 100

print(f"Implied volatility (India VIX) : {vix:.2f}%")
print(f"Realized volatility (last 30d) : {realized:.2f}%")
print(f"Volatility risk premium        : {vix - realized:+.2f}%")
print("\nImplied usually exceeds realized - the premium that option SELLERS harvest for bearing risk.")
print("Like insurance: buyers overpay for protection on average, sellers collect it - until a crash.")
```

Live output

```
Implied volatility (India VIX) : 13.39%
Realized volatility (last 30d) : 11.76%
Volatility risk premium        : +1.63%

Implied usually exceeds realized - the premium that option SELLERS harvest for bearing risk.
Like insurance: buyers overpay for protection on average, sellers collect it - until a crash.
```

India VIX implies 13.4%, but the market actually delivered under 12% - a **volatility risk premium** of about +1.6%. This gap is persistent and structural: option _buyers_ are buying insurance and willingly overpay for protection, while option _sellers_ collect that premium for bearing the risk - exactly like an insurance company. Selling volatility harvests this premium, and it's one of the most reliable income strategies in markets... with a terrifying catch we'll come to.
## Buy versus sell volatility
The two sides of the vol trade are mirror images, and you must know which you're on:
Buy volatility (long) + pays the premium + positive gamma, negative theta + profits from BIG moves + loss limited to the premium wants a storm Sell volatility (short) + collects the premium + negative gamma, positive theta + profits from CALM + rare but huge tail loss wants quiet - harvests the premium The two sides of a volatility trade
The buyer has **positive gamma** (gains as the market moves, either way) but bleeds **theta** every day. The seller is the reverse: pocketing theta daily but exposed to **negative gamma** - small steady gains, then a sudden brutal loss if the market lurches. The volatility risk premium is the seller's reward for standing on that trapdoor.
## Gamma scalping
There's a purer way to trade the implied-versus-realized gap: **gamma scalping**. Hold a long-gamma position (like the straddle) and continuously **delta-hedge** it - buying the underlying when it dips, selling when it rises. Each hedge locks in a small profit from the market's wiggles. If the volatility you actually capture (realized) exceeds what you paid (implied), you win; if not, theta grinds you down. It's the cleanest expression of "I think realized vol will beat implied," and it's a staple of professional options desks.
## Expiry-day games
India puts its own stamp on all of this through **weekly expiries**. On expiry day, time decay is savage - an option's entire remaining value evaporates in hours - so enormous flows of premium-selling concentrate there, and the underlying can get "pinned" near a heavily-traded strike. The risk-reward warps: sellers harvest fat theta, but a sudden move can inflict outsized losses in minutes. A huge share of India's record options volume is this weekly expiry-day vol-selling - and a whole family of quant strategies (Module G) is built around its rhythm.
Heads up
Selling volatility is famously "picking up pennies in front of a steamroller." The income is steady and the win rate is high - which is exactly what makes it dangerous, because it lulls you into sizing up right before the rare day the steamroller arrives. Many blow-ups in history were naked vol sellers. If you sell vol, **defined risk and hard position limits aren't optional** - they're the whole strategy.
## Try it yourself
  * Build a _short_ straddle payoff (flip the sign). Confirm it's an inverted V - steady profit if Nifty sits near the strike, escalating loss if it runs.
  * Track the vol risk premium daily for a week. Is implied consistently above realized, and does the gap shrink when the market gets turbulent?
  * Compare a weekly-expiry straddle's cost to a monthly one. How much cheaper is the weekly - and how much less room does it give the market to move?


## Recap
  * You can trade **volatility itself** - a **straddle** buys or sells a big move with no directional view.
  * A **long straddle** profits if the market moves beyond its breakevens; its worst case is a calm market that wastes the premium.
  * The **volatility risk premium** - implied vol usually exceeds realized (+1.6% here) - is the structural edge that option _sellers_ harvest, like insurers.
  * **Long vol** is positive-gamma/negative-theta (wants storms); **short vol** is the reverse (wants calm, collects premium, carries tail risk); **gamma scalping** trades the implied-vs-realized gap directly.
  * India's **weekly expiries** concentrate vicious theta decay and pin risk into expiry day - huge volume, huge opportunity, and the ever-present **steamroller** that makes risk limits non-negotiable.


That completes Module F - we've priced options with Black-76, read the volatility surface, and traded vol itself. Now we zoom out from the single trade to the whole **portfolio** : how to combine many positions so that diversification, sizing and risk control turn a collection of edges into a survivable book.
On this page
