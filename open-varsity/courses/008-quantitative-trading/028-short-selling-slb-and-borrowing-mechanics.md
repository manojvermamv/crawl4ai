Chapters
Module C · Indian Market Microstructure - Chapter 28
# Short Selling, SLB and Borrowing Mechanics
How shorting really works in India - intraday vs delivery shorts, the securities lending and borrowing market, and the cost and risk of being short.
NSENFO
What you'll learn
  * ·Intraday vs delivery shorts
  * ·SLB mechanics
  * ·Borrow cost and availability
  * ·Short squeezes
  * ·Naked short rules in India
  * ·Shorting for market-neutral books


Going long and going short are not mirror images. To buy a share you need cash. To sell a share you do not own, you need the share itself - borrowed from someone who has it, with a promise to give it back on time. That asymmetry, plus an Indian rule that you may never sell a share you have not actually arranged to deliver, quietly shapes every short you will ever put on. Before you can trade a single short-side signal, you have to understand the plumbing underneath it.
## Three ways to be short
There are three routes onto the short side, each with different plumbing.
**Intraday shorting** is the simplest. Sell first and buy back before the close in the same session, under an intraday product, and no borrow is needed - the exchange nets your sell against your buy and you never have to deliver a share. The catch is obvious: you cannot carry the position overnight. The closing bell forces you flat.
**Delivery shorting** means holding a short past the close in the cash market. Now settlement bites. On T+1 you are obliged to deliver shares you do not own, so you must borrow them first, through the SLB market below. Sell without arranging that borrow, fail to deliver, and the trade goes to the exchange auction where you are bought in at a penalty that can dwarf the trade.
**Synthetic shorting** uses derivatives. Sell a stock future, or build a short with options, and you are short the name without ever touching a physical share. Most quant shorts in India ride futures, because the cost of borrowing is baked cleanly into the futures price and there is no share to source.
Heads up
India bans **naked short selling** - selling a security you have not arranged to deliver. Every overnight cash short must be backed by a genuine borrow; institutions disclose the short upfront, retail discloses it at the time of the order. Fail to deliver and the position is bought in at auction, often at a punitive price. The no-naked-short rule is precisely why the SLB market has to exist.
## The SLB market
**SLB** stands for securities lending and borrowing - an exchange-run, clearing-corporation-guaranteed marketplace where holders of stock lend it out for a fee and short sellers borrow it to deliver. The economics are simple. A long-term holder - an index fund, an insurer, a patient investor - has idle shares sitting in the demat account doing nothing. By lending them out, the holder earns an extra yield for taking on what is essentially operational risk. The borrower pays that fee for the right to sell a share they will buy back and return later.
The crucial design feature is **novation** : the clearing corporation steps in as the counterparty to both legs. The lender does not face the short seller's credit; they face the clearing corp, which guarantees the return of the stock. That is what makes lending to anonymous strangers safe enough to be worth a few percent a year.
Lender long-term holder, earns fee SLB platform clearing corp guarantees Short seller sells now, owes shares lends delivers borrow buy back, return shares + borrow fee The securities lending and borrowing cycle
The borrow fee is quoted as an annualised lending rate, and it floats with supply and demand. A liquid large cap that everyone holds and few want to short is **easy to borrow** and costs almost nothing. A small or heavily shorted name, where lenders are scarce and borrowers many, is **hard to borrow** , and the fee can spike into double digits annualised - or the stock simply becomes unavailable at any price.
Note
Lending is a yield play on inventory you were holding anyway. The lender keeps economic ownership - they still receive the dividend, which the borrower must pass through, and they retain the right to recall the stock - so for a buy-and-hold book SLB is close to free money. The flip side is that recall right, which becomes the short seller's nightmare in a squeeze.
## What a short really costs
Add it all up and the honest cost of carrying a short is the borrow fee, plus any dividend you must pass through to the lender, plus the financing cost of cash you receive but cannot freely use. For a quant, the cleanest way to see all of this in a single number is to forget the stock and look at the **future**.
Sell the near-month future instead of borrowing stock, and the future's **basis** - its gap to spot - is the market's own quote for the cost of carry. Selling a future that trades above spot means you collect that premium and earn it back as the future converges to spot at expiry.
EX 1The cost of carry of a short, read from the basisNSENFOch28/01_short_carry.py
Copy
```
# Cost of carry of a short held via the near-month future: basis -> implied annualised carry.
import math
import os
from datetime import datetime, timedelta

import pandas as pd
from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

SPOT, FUT, EXPIRY = "RELIANCE", "RELIANCE28JUL26FUT", datetime(2026, 7, 28)
end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=45)).strftime("%Y-%m-%d")

s = client.history(symbol=SPOT, exchange="NSE", interval="D", start_date=start, end_date=end)
f = client.history(symbol=FUT, exchange="NFO", interval="D", start_date=start, end_date=end)
j = pd.DataFrame({"spot": s["close"], "fut": f["close"]}).dropna()

asof = j.index[-1]
S, F = j["spot"].iloc[-1], j["fut"].iloc[-1]
days = (EXPIRY - asof).days
T = days / 365.0

basis = F - S
basis_pct = (F / S - 1) * 100
carry_ann = math.log(F / S) / T * 100  # continuous, annualised
avg_basis = (j["fut"] - j["spot"]).mean()

print(f"As of {asof.date()}   spot {S:,.1f}   {FUT} {F:,.1f}")
print(f"Basis (future - spot): {basis:+.2f} pts  ({basis_pct:+.2f}%),  {days} days to expiry")
print(f"Avg basis over window: {avg_basis:+.2f} pts")
print(f"Implied annualised carry: {carry_ann:+.2f}%")
sign = "positive carry - it earns" if basis > 0 else "negative carry - it pays"
print(f"A short via the future sells the {basis_pct:+.2f}% premium, so the short has {sign} ~{abs(carry_ann):.2f}% annualised as the future converges to spot.")
```

Live output

```
As of 2026-06-25   spot 1,318.1   RELIANCE28JUL26FUT 1,323.6
Basis (future - spot): +5.50 pts  (+0.42%),  33 days to expiry
Avg basis over window: +13.55 pts
Implied annualised carry: +4.61%
A short via the future sells the +0.42% premium, so the short has positive carry - it earns ~4.61% annualised as the future converges to spot.
```

As of 2026-06-25, RELIANCE spot was 1,318.1 and the 28 July future 1,323.6 - a basis of +5.50 points, or +0.42%, with 33 days to expiry. Annualised, that is an implied carry of about +4.61%. Because the future sits at a premium (contango), a short put on through the future sells that premium and pockets it as the contract grinds down to spot by expiry. The short earns roughly 4.61% annualised from convergence alone, before any view on direction. Note too that the average basis over the window was +13.55 points: the premium has been compressing as expiry approaches, exactly as carry theory predicts.
Key idea
The sign of the basis decides whether carry helps or hurts a short. Short a name in **contango** (future above spot) and convergence pays you. Short a name in **backwardation** (future below spot) and convergence costs you, on top of any borrow fee. Always check the basis before you assume a short is cheap.
## Short squeezes and recall risk
A long can only go to zero; a short's loss is unbounded, and that asymmetry has a violent failure mode. When a heavily shorted stock starts to rise, the shorts who are bleeding are forced to buy back to cap their losses. That buying pushes the price up further, forcing the next tier of shorts to cover, and the feedback loop becomes a **short squeeze**. At the same time borrow availability dries up, fees spike, and lenders exercise their recall right - forcing you to return shares you do not have and to buy them in at the worst possible moment.
The footprint is unmistakable: a sharp, almost vertical up-move riding a surge of volume well above normal, as forced covering and momentum buyers pile in together.
EX 2Spotting a short-squeeze footprint in price and volumeNSEch28/02_short_squeeze.py
Copy
```
# A short-squeeze candidate: a sharp up-move on a surge of volume (forced covering).
import os
from datetime import datetime, timedelta
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

SYMBOL = "SBIN"
end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=220)).strftime("%Y-%m-%d")
df = client.history(symbol=SYMBOL, exchange="NSE", interval="D", start_date=start, end_date=end)

df["ret"] = df["close"].pct_change()
peak = df["ret"].idxmax()
volx = df["volume"] / df["volume"].median()

sns.set_theme(style="whitegrid")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5.2), sharex=True, gridspec_kw={"height_ratios": [2.6, 1]})
ax1.plot(df.index, df["close"], color="#7c83ff", lw=1.7)
ax1.scatter([peak], [df.loc[peak, "close"]], color="#dc2626", s=70, zorder=5,
            label=f"+{df.loc[peak, 'ret'] * 100:.1f}% on {peak.date()}")
ax1.set_ylabel("Price (Rs)")
ax1.set_title(f"{SYMBOL} - sharp up-move on a volume surge (squeeze candidate)")
ax1.legend(loc="upper left")

colors = ["#dc2626" if v >= 2 else "#9aa0aa" for v in volx]
ax2.bar(df.index, df["volume"] / 1e6, color=colors, width=1.0)
ax2.set_ylabel("Volume (M)")

out = Path(__file__).with_suffix(".png")
plt.savefig(out, dpi=110, bbox_inches="tight")
print(f"{SYMBOL} jumped {df.loc[peak, 'ret'] * 100:.1f}% on {peak.date()} at {volx.loc[peak]:.1f}x median volume - a classic short-squeeze signature. Saved {out.name}")
```

Live output

```
SBIN jumped 7.5% on 2026-02-09 at 3.0x median volume - a classic short-squeeze signature. Saved 02_short_squeeze.png
```

![Spotting a short-squeeze footprint in price and volume chart](https://openalgo.in/quant/charts/ch28_02_short_squeeze.png)
The script flags the single biggest up-day in the window and checks the volume behind it. SBIN jumped 7.5% on 2026-02-09 at 3.0x its median volume - a textbook squeeze signature, where a cluster of forced buying shows up as a price spike sitting on an abnormal volume bar. Whether that exact move was a true squeeze or just a powerful rally, the pattern is the one to respect: large gap up, huge volume, and a borrow that suddenly turns expensive.
Heads up
Never carry a short without a hard stop and a plan for recall. Size the position assuming the loss is open-ended, that the borrow can be pulled, and that you may be bought in at the high of the move. A short that is "right" on the fundamentals can still ruin you if the squeeze arrives before the thesis plays out.
## Shorting for a market-neutral book
Most professional shorting is not a directional bet at all. It is one leg of a hedge. Long-short equity, the pairs trades of Chapter 45, and the index arbitrage of Chapter 50 all depend on a reliable, cheap, repeatable short. The borrow then becomes a hard constraint on the strategy: a beautiful long-short signal is worthless if the short leg costs 15% a year to borrow or cannot be sourced at all.
Tip
Systematic short books in India lean on futures for exactly this reason. The borrow cost is transparent - it is just the basis you can read off a screen - and there is no SLB sourcing risk. The price you pay is universe: stock futures exist only for the F&O-eligible names, so a futures-only neutral book can short roughly that list and nothing else.
So the mechanics of borrowing quietly decide what a market-neutral book can even hold. Capacity, turnover and the choice of names all bend around where the borrow is cheap and deep. Outside the F&O list you are back to SLB availability, or you simply cannot short the name - and that is a strategy design fact, not an afterthought.
## Recap and the road ahead
  * A short can be **intraday** (no borrow, must square off), **delivery** (must borrow via SLB to deliver), or **synthetic** (sell a future or use options).
  * India bans **naked shorting** : every overnight cash short needs a real borrow, or it goes to auction with a penalty.
  * The **SLB market** lets holders lend idle stock for a fee, with the clearing corp guaranteeing the return through novation; the fee floats from near-zero for easy-to-borrow names to double digits for hard-to-borrow ones.
  * Read the true cost of a short from the **basis** : contango pays the short through convergence, backwardation costs it.
  * **Short squeezes** and **recall** make a short's risk open-ended, so size for the tail, not the thesis.


That closes Module C. We have climbed the whole microstructure ladder - from the order book and price-time priority, through the trading day, impact cost and order flow, to the borrowing plumbing beneath a short. Next, in Module D, we change gears from how the market works to how we act inside it at speed: algorithmic execution, HFT, and the technology that turns a signal into a fill.
On this page
