Chapters
Module F · Derivatives, Volatility & Arbitrage - Chapter 49
# Futures, Forwards and Cost of Carry
The most powerful idea in pricing - no free money - and how cost of carry sets the fair price of a future against its underlying.
NFOINDEX
What you'll learn
  * ·Forwards vs futures
  * ·The no-arbitrage principle
  * ·Cost of carry
  * ·Fair value and basis
  * ·Convergence at expiry
  * ·Carry in Indian futures


We arrive at derivatives - the most mathematical corner of markets, and the one where India does things its own way. Module F opens not with options but with the instrument everything else is priced against: the **future**. And the whole of futures pricing rests on one almost philosophical idea: **free money cannot exist**. If two things deliver the same payoff, they must cost the same today, or someone would buy the cheap one, sell the dear one, and pocket a riskless profit until the prices snapped together. That refusal to leave free money on the table is **no-arbitrage** , and it is the gravity that fixes the price of every future. Master it here and the rest of the module - the basis trade, options, the Greeks - has a foundation to stand on.
## Forwards and futures
Start with the contract itself. A **forward** is a private agreement to buy something at a future date for a price fixed now. A **future** is the same promise, but standardised and traded on an exchange, with the clearing corporation stepping between buyer and seller so neither carries the other's credit risk. Three practical differences matter to a quant:
  * A forward is bespoke and over-the-counter; a future is a listed contract with fixed lot size and expiry (NIFTY28JUL26FUT, RELIANCE28JUL26FUT).
  * A future is **marked to market daily** : gains and losses settle into your margin account every evening, so no large credit exposure builds up toward expiry. A forward settles only once, at the end.
  * The clearing corporation **novates** the future (Chapter 7), guaranteeing performance; a forward leaves you exposed to your counterparty.


For pricing, though, the two are almost identical. Daily settlement introduces a tiny convexity adjustment that depends on how interest rates correlate with the underlying, but for the horizons and rates of Indian equity F&O it is negligible. So we can price a future with the same forward logic and call the result the **forward price** without losing anything that matters.
Note
A forward and a future on the same asset for the same date carry essentially the same price. Their differences - daily mark-to-market, exchange clearing, standardised terms - are about _credit and liquidity_ , not _value_. Throughout this module "the forward" means the fair price either contract should trade at.
## The no-arbitrage principle
State it plainly: if two portfolios have identical future payoffs, they must have identical prices _today_. Any gap is an **arbitrage** - a money pump - and in liquid markets, armies of traders (and the HFT desks of Module D) close such gaps in milliseconds. So the gaps do not persist, which means we can _derive_ the fair price of a future by building an equivalent portfolio and insisting the prices match. No forecasting, no opinion, just the refusal to leave free money on the table.
## Cost of carry and fair value
Apply that to a future and the fair price falls right out. Buying the future should cost the same as buying the asset today and holding it to expiry. Holding is not free: you tie up money (a **financing cost**) but you may also earn income (dividends on a stock or basket). So the fair future price is **spot plus the cost of carry** - the net of financing minus income over the life of the contract:
fair future = spot + financing - income
The gap between the future and spot is the **basis** , and it is simply the cost of carry made visible. Read it off the live NIFTY contract:
EX 1The basis: future minus spotINDEXNFOch49/01_basis.py
Copy
```
# The basis: how far the future trades from spot - and why no-arbitrage sets it.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

spot = client.quotes(symbol="NIFTY", exchange="NSE_INDEX")["data"]["ltp"]
fut = client.quotes(symbol="NIFTY30JUN26FUT", exchange="NFO")["data"]["ltp"]
basis = fut - spot

print(f"NIFTY spot   : {spot:.2f}")
print(f"NIFTY future : {fut:.2f}")
print(f"Basis (future - spot): {basis:+.2f}   ({'premium' if basis > 0 else 'discount'})")
print(f"As % of spot : {basis / spot * 100:+.2f}%")
print("\nNo-arbitrage ties them: future = spot + cost of carry.")
print("They MUST converge as expiry approaches - if they didn't, it would be free money.")
```

Live output

```
NIFTY spot   : 24021.65
NIFTY future : 24053.60
Basis (future - spot): +31.95   (premium)
As % of spot : +0.13%

No-arbitrage ties them: future = spot + cost of carry.
They MUST converge as expiry approaches - if they didn't, it would be free money.
```

Nifty's future trades at a small premium to spot: the +32 basis (24054 future against 24022 spot) is essentially the cost of carrying the index to expiry. Divide that gap by the days remaining and you recover the market's implied financing rate, net of the dividend yield it expects to collect. That annualised carry is the right yardstick - a raw point gap means nothing until you put it per unit of time.
Key idea
The fair price of a future is **spot plus the cost of carry** (financing minus income). The basis - future minus spot - is that carry quoted in points. Always annualise it before judging whether a future is rich or cheap.
## Convergence at expiry
Here is the punchline that keeps the future honest. As expiry approaches, there is less and less time left to carry the asset, so the cost of carry shrinks - and at expiry it is zero. The future and spot are therefore _forced_ to converge: on the last day the future simply _is_ spot, because a contract to buy "in zero time" is just a contract to buy now. If the two ever drifted apart near expiry, you could buy the cheap leg, sell the dear one, and collect the difference for no risk, so the market never lets it survive.
This convergence is the engine behind the **cash-futures basis trade** and **index arbitrage** : sell the future when its basis is rich, buy the underlying basket, and let convergence hand you the locked-in carry. That trade - its mechanics, its dividend subtleties and its very real frictions - gets its own chapter next (Chapter 50). Here the point is narrower and more fundamental: convergence is _why_ the cost-of-carry formula holds at all.
Tip
A near-dated future and spot must meet at expiry, so the raw basis mechanically shrinks as the contract ages. That is exactly why you annualise it: a 100-point basis with two months to run and the same gap with two days to run imply wildly different carries.
## Carry in Indian futures
In Indian equity futures the carry is almost always _positive_ - the future trades above spot - because the financing cost of holding the basket usually outweighs the dividends it pays before expiry. A few features colour the Indian picture:
  * **Index versus single stock.** A NIFTY future's carry nets money-market financing against the dividend yield of the 50-stock basket. A single-stock future like RELIANCE28JUL26FUT carries financing on that one name minus its own expected dividend, so a stock about to go ex-dividend can show a noticeably thinner, even negative, basis.
  * **Dividends hide in the carry.** When a heavy constituent goes ex-dividend, spot drops but the future barely moves (it never had a claim on that dividend), so the basis narrows around big payout dates. Mistaking that for a "cheap" future is a classic error.
  * **Demand and squeeze.** Carry is not a pure interest rate. Heavy long interest in a popular future can push its basis above fair financing; aggressive shorting, or hard-to-borrow stock, can push it below. The basis carries information about positioning, not just rates, a theme we return to in the flow chapter (Chapter 64).
  * **Roll cost.** A position held past expiry must be rolled to the next contract, paying the carry again. For a systematic book that carries futures month after month, this roll is a real, recurring cost, not an afterthought.


Heads up
Cost of carry is reliable in _direction_ - the basis converges to zero at expiry - but noisy in _level_. Rates, the dividend schedule and raw supply and demand all move it day to day. Treat the carry as a live, market-implied number to be re-measured, never a constant you can hard-code.
## From the forward to options: the synthetic future
We now have a forward price, built from carry and pinned down by convergence. It turns out there is a second, entirely different route to the same forward - one made purely from options. **Put-call parity** ties a call and a put at the same strike together so tightly that buying the call, selling the put and adding the strike reproduces a long forward exactly. That construction is the **synthetic future** , and it lands on the same number the actual future does:
EX 2Building a synthetic futureINDEXNFOch49/02_synthetic_future.py
Copy
```
# Put-call parity builds a 'synthetic future' from options - the Black-76 forward.
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

# The synthetic future = ATM strike + ATM call price - ATM put price (put-call parity).
sf = client.syntheticfuture(underlying="NIFTY", exchange="NSE_INDEX", expiry_date="30JUN26")
spot = sf["underlying_ltp"]
synthetic = sf["synthetic_future_price"]
fut = client.quotes(symbol="NIFTY30JUN26FUT", exchange="NFO")["data"]["ltp"]

# A zoomed bar chart: spot sits just below the future and synthetic (the cost of carry).
sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(7, 4.2))
labels = ["Spot", "Synthetic\nfuture", "Actual\nfuture"]
vals = [spot, synthetic, fut]
sns.barplot(x=labels, y=vals, hue=labels, legend=False,
            palette=["#888", "#16a34a", "#7c83ff"], ax=ax)
ax.set_ylim(min(vals) - 25, max(vals) + 15)        # zoom in to see the small gaps
for i, v in enumerate(vals):
    ax.text(i, v + 1, f"{v:.0f}", ha="center", fontsize=10)
ax.set_title("Spot vs synthetic future vs actual future")
ax.set_ylabel("NIFTY level")
plt.savefig(Path(__file__).with_suffix(".png"), dpi=110, bbox_inches="tight")

print(f"Spot LTP          : {spot:.2f}")
print(f"ATM strike        : {sf['atm_strike']:.0f}")
print(f"Synthetic future  : {synthetic:.2f}   (= strike + ATM call - ATM put)")
print(f"Actual future     : {fut:.2f}")
print(f"Synthetic vs real : {synthetic - fut:+.2f} difference")
print("\nThe synthetic future, built purely from option prices, tracks the real future -")
print("and it is the FORWARD that Indian F&O Greeks are priced against (Black-76, next chapter).")
```

Live output

```
Spot LTP          : 24021.65
ATM strike        : 24000
Synthetic future  : 24058.30   (= strike + ATM call - ATM put)
Actual future     : 24053.60
Synthetic vs real : +4.70 difference

The synthetic future, built purely from option prices, tracks the real future -
and it is the FORWARD that Indian F&O Greeks are priced against (Black-76, next chapter).
```

![Building a synthetic future chart](https://openalgo.in/quant/charts/ch49_02_synthetic_future.png)
Synthetic future strike + call - put 24058 ≈ Actual future NFO 24054 ≈ Spot + carry 24022 + ~32 24054 No-arbitrage forces the synthetic, the future and spot-plus-carry together
The synthetic future (24058), assembled entirely from option prices, sits within a handful of points of the real future (24054), which in turn is spot plus carry. Three routes, one forward, all welded together by no-arbitrage. We only sketch the idea here. Put-call parity and the synthetic future deserve - and get - their own full treatment in the options-pricing chapter, where they become the foundation for pricing options correctly in India.
Key idea
Indian index and stock options settle against the **futures/forward** , not spot. So the right underlying to feed an options model is this forward, best read as the synthetic future from put-call parity, which is exactly why Indian F&O is priced with **Black-76** (built for options on a forward), not vanilla Black-Scholes off spot. We take put-call parity and the synthetic future much further in the options-pricing chapter (Chapter 51).
## Recap
  * A **forward** is an over-the-counter promise to buy later at a price fixed now; a **future** is its exchange-traded, daily-marked, centrally-cleared twin - same value, different credit and liquidity.
  * **No-arbitrage** - free money cannot exist - fixes the fair future at **spot plus the cost of carry** (financing minus income). The basis is that carry in points; always annualise it.
  * The basis is **forced to zero at expiry** : with no time left to carry, the future simply becomes spot. That convergence is the engine of the basis trade, covered next (Chapter 50).
  * In Indian futures the carry is usually positive, shaped by financing, dividends, demand and roll cost - reliable in direction, noisy in level.
  * A **synthetic future** from put-call parity reaches the same forward from options; because Indian F&O settles against that forward, options are priced with **Black-76** , explored fully next (Chapter 51).


We have built the forward that the whole module is priced against, and seen the two ways the market reaches it: carry on the cash side, parity on the options side. Next we put the cash side to work - the cash-futures basis, when it is rich or cheap, and the index arbitrage that keeps the future honest.
On this page
