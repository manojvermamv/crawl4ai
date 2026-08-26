Chapters
Module F · Derivatives, Volatility & Arbitrage - Chapter 50
# Cash-Futures Basis and Index Arbitrage
The arbitrage that runs on every Indian desk - the cash-futures basis, when it is rich or cheap, and how index arbitrage keeps the future honest.
NFOINDEX
What you'll learn
  * ·The cash-futures basis
  * ·Rich vs cheap basis
  * ·Index arbitrage mechanics
  * ·Replicating the index
  * ·Dividends and the basis
  * ·Risks of basis trades


Every Indian trading desk runs a quiet little machine in the background, one that almost never makes headlines but underpins the whole derivatives market: the cash-futures arbitrage. It watches one number obsessively - the gap between the index future and the index itself - and it pounces whenever that gap drifts away from fair value. The gap is called the **basis** , and learning to read it is the difference between treating the future as a mysterious separate instrument and seeing it for what it really is: spot, plus a precisely calculable cost of carry, dragged inexorably back to spot at expiry. This chapter is about that basis, when it is rich or cheap, and the arbitrage that keeps the future honest.
## The cash-futures basis
In Chapter 49 we established the law: a future equals spot plus the **cost of carry** - the interest on the money you would tie up buying the asset today, minus any income (dividends) you would earn holding it. The **basis** is simply that carry made visible: future price minus spot price. For an index it is almost always positive (the future trades at a _premium_), because the financing cost of carrying the basket usually outweighs the dividends the basket throws off.
Let us measure it on the live near-month NIFTY contract.
EX 1The basis and the carry it impliesINDEXNFOch50/01_basis_carry.py
Copy
```
# The cash-futures basis and the annualised carry it implies (cost-of-carry / Black-76).
import os
from datetime import date
from math import log

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# Near monthly contract: NIFTY future expiring 28 Jul 2026.
EXPIRY = date(2026, 7, 28)
spot = client.quotes(symbol="NIFTY", exchange="NSE_INDEX")["data"]["ltp"]
fut = client.quotes(symbol="NIFTY28JUL26FUT", exchange="NFO")["data"]["ltp"]

basis = fut - spot                       # points the future trades above spot
days = (EXPIRY - date.today()).days      # calendar days to expiry
T = days / 365.0
# F = S * exp(carry * T)  ->  carry = ln(F/S) / T  (net of dividend yield)
carry = log(fut / spot) / T

print(f"NIFTY spot            : {spot:.2f}")
print(f"NIFTY 28JUL26 future  : {fut:.2f}")
print(f"Basis (future - spot) : {basis:+.2f} pts  ({basis / spot * 100:+.2f}% of spot)")
print(f"Days to expiry        : {days}")
print(f"Annualised net carry  : {carry * 100:.2f}%   (rate minus dividend yield)")
print(
    f"SUMMARY: basis {basis:+.1f} pts over {days} days implies "
    f"{carry * 100:.2f}% annualised carry."
)
```

Live output

```
NIFTY spot            : 24056.00
NIFTY 28JUL26 future  : 24170.50
Basis (future - spot) : +114.50 pts  (+0.48% of spot)
Days to expiry        : 30
Annualised net carry  : 5.78%   (rate minus dividend yield)
SUMMARY: basis +114.5 pts over 30 days implies 5.78% annualised carry.
```

With NIFTY spot at 24056.00 and the 28 July future at 24170.50, the basis is **+114.50 points** , just under half a percent of spot. On its own that number is meaningless - a 114-point basis with two days left would be enormous, the same basis with two years left would be tiny. What matters is the basis _per unit time_ , which we annualise: 114.5 points over 30 days works out to a **5.78% annualised net carry**. That is the market's implied financing rate for holding the index, net of the dividend yield it expects to receive before expiry. It should sit close to the short-term money-market rate minus the index dividend yield, and 5.78% is exactly the right neighbourhood.
Key idea
The basis is not a forecast and it is not sentiment. It is the **cost of carry** quoted in points. Always annualise it before judging it - a fair basis shrinks mechanically as expiry nears, so the raw point gap tells you nothing until you divide by time.
## Rich, cheap, and the fair-value line
Cost of carry gives us a **fair-value basis** for any moment: take spot, apply the financing rate for the days remaining, subtract the dividends expected in that window. Compare the _traded_ basis to that fair value and you can label the future:
  * **Rich** (future trades above fair value): the future is expensive relative to spot. The arbitrageur _sells the future_ and _buys the basket_ - a **cash-and-carry** trade. They lock in the rich carry, hold to expiry, and the position unwinds at convergence for a near-riskless profit.
  * **Cheap** (future trades below fair value): the future is too low. The arbitrageur _buys the future_ and _sells the basket_ (a **reverse cash-and-carry**), often funded by lending the stock or unwinding an existing long.


Neither trade needs a view on where NIFTY is going. The profit is the _mispricing in the basis_ , captured at expiry when the future and spot are forced together. This is the cleanest expression of the no-arbitrage gravity from Chapter 49, and it is why the basis rarely strays far: the moment it does, this machine sells the rich side and buys the cheap side until the gap closes.
Tip
A quick sniff test: convert the traded basis to an annualised rate, as the example does, and compare it to the prevailing short rate minus the dividend yield. A future implying 9% carry when money costs 6% is _rich_ ; one implying 3% is _cheap_. The annualised carry is your fair-value yardstick.
The basis converges to zero at expiry NIFTY level Future Spot basis = carry expiry basis -> 0 time -> The future starts above spot by the cost of carry; no-arbitrage drags the gap to zero at expiry
## Index arbitrage mechanics
To actually _do_ the cash side of this trade, you cannot buy "NIFTY" - there is no such tradable thing. You must **replicate the index** : build a basket of the 50 constituents in their exact index weights. RELIANCE, HDFCBANK, ICICIBANK, INFY and the rest, each sized so the basket's profit and loss tracks the index point for point. Buy that basket, simultaneously sell one NIFTY future against it, and you hold a hedged, market-neutral position whose only moving part is the basis. Hold to expiry; the future converges to spot; you unwind and bank the carry you locked in.
The same Black-76 logic from the synthetic future in Chapter 49 applies here. The future, the synthetic future built from options, and spot-plus-carry are three routes to one **forward** price. Index arbitrage is what physically enforces that equality in the cash market, while options market-makers enforce it through put-call parity. Both are pushing the same forward into line.
Note
Replication is rarely perfect. Most desks track the index with a _representative subset_ of the heaviest names, or with index ETFs, accepting a little **tracking error** in exchange for far lower transaction costs than trading all 50 stocks. The trade-off between replication fidelity and cost is itself a quant problem, revisited in the portfolio module (Chapter 71).
## Dividends hide inside the basis
Here is the subtlety that trips up newcomers. The carry we back out is a _net_ number: financing cost **minus** the dividend yield the basket pays before expiry. When a large constituent goes ex-dividend, the index drops by the dividend but the future barely moves, because the future never had a claim on that dividend in the first place. So the basis _narrows_ around big dividend dates, and the implied carry dips. A trader who mistakes a dividend-driven narrowing for a "cheap" future, and buys it expecting the basis to widen back, is simply collecting the dividend they forgot to subtract. Getting the expected-dividend schedule right is most of the real work in pricing the fair-value basis - especially in March quarter and around heavy-payout names.
## Convergence, and the risks that bite
The defining feature of the basis is that it **must** go to zero at expiry. Watch it happen on the contract that is expiring right now.
EX 2The basis converging into expiryINDEXNFOch50/02_basis_convergence.py
Copy
```
# The basis collapses to zero as expiry nears: NIFTY June future minus spot over its life.
import os
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

# The June contract is expiring now, so we can watch its full convergence.
START, END = "2026-04-01", "2026-06-28"
spot = client.history(symbol="NIFTY", exchange="NSE_INDEX", interval="D",
                      start_date=START, end_date=END)["close"]
fut = client.history(symbol="NIFTY30JUN26FUT", exchange="NFO", interval="D",
                     start_date=START, end_date=END)["close"]

basis = (fut - spot).dropna()            # points of premium, day by day

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(8, 4.4))
ax.plot(basis.index, basis.values, color="#7c83ff", lw=1.8, label="basis = future - spot")
ax.fill_between(basis.index, basis.values, 0, color="#7c83ff", alpha=0.12)
ax.axhline(0, color="#dc2626", lw=1.1, ls="--", label="expiry: basis -> 0")
ax.set_title("NIFTY June future: the basis converges toward expiry")
ax.set_ylabel("Basis (points)")
ax.legend(loc="upper right")
fig.autofmt_xdate()
plt.savefig(Path(__file__).with_suffix(".png"), dpi=110, bbox_inches="tight")

print(
    f"SUMMARY: NIFTY June basis fell from {basis.iloc[0]:+.0f} pts on "
    f"{basis.index[0].date()} to {basis.iloc[-1]:+.0f} pts by "
    f"{basis.index[-1].date()} as expiry approached."
)
```

Live output

```
SUMMARY: NIFTY June basis fell from +398 pts on 2026-04-01 to +46 pts by 2026-06-25 as expiry approached.
```

![The basis converging into expiry chart](https://openalgo.in/quant/charts/ch50_02_basis_convergence.png)
The June NIFTY future's basis fell from **+398 points on 1 April to +46 points by 25 June** as expiry approached - a textbook convergence, the carry bleeding out day by day exactly as no-arbitrage demands. That decay is reliable in direction but noisy in detail, and that noise is where the risk lives:
  * **Basis risk.** Before expiry, the basis can move _against_ you even when your hedge is "market neutral". A cash-and-carry locked at a rich basis still suffers mark-to-market losses if the basis richens further first. You are right at expiry, but you must survive the path.
  * **Dividend risk.** An unexpected special dividend, or a change to the expected schedule, shifts fair value under your feet. Your "riskless" carry was only as good as your dividend forecast.
  * **Execution and cost.** The edge in index arbitrage is _thin_ - a few points of mispricing against fifty bid-ask spreads, impact, securities transaction tax, and financing. As Chapter 26 warned, most of the gap you see on screen is eaten by the cost of crossing it. Legging risk (filling the basket but missing the future, or vice versa) can wipe out the whole trade.
  * **Funding and shorting frictions.** The reverse trade needs you to short the basket, which means borrowing stock at a rate that may exceed the cheapness you spotted.


Heads up
The cash-futures basis looks like free money and almost never is. The pure arbitrage belongs to desks with the lowest financing, the best execution, and a precise dividend model. For everyone else, the real value of the basis is as a _signal_ - a clean, market-implied read on carry, dividends and demand - not as a trade you can lift off the screen.
We now have the forward fully pinned down: built from carry, enforced by arbitrage, and converging at expiry. With that forward in hand, the next chapter turns to the instruments priced _against_ it - why Indian options use **Black-76 off this forward** , not Black-Scholes off spot, and how that single choice ripples through every Greek that follows.
On this page
