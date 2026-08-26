Chapters
Module F · Derivatives, Volatility & Arbitrage - Chapter 58
# Margins, Collateral, Position Limits and Settlement
The capital machinery of derivatives - SPAN and exposure margin, collateral and haircuts, position limits, and physical settlement of stock F&O.
NFO
What you'll learn
  * ·SPAN and exposure margin
  * ·Collateral and haircuts
  * ·Cross-margin benefits
  * ·Position limits
  * ·Physical settlement
  * ·Margin in a quant book


Derivatives give you a remarkable gift and an equally remarkable trap, and they are the same thing: **leverage**. One lot of the NIFTY future controls about Rs 15.7 lakh of index, yet you part with only Rs 1.78 lakh to hold it. That is roughly nine rupees of exposure for every rupee you post. The exchange is not being generous - it has run a worst-case loss simulation on your position and decided that buffer is enough to survive almost any single day. This final chapter of the derivatives module is about that buffer: how margin is computed, what collateral you can post against it, the limits on how big you may get, how stock contracts actually settle, and why a serious quant treats margin not as paperwork but as a hard constraint that shapes every position.
## SPAN and exposure: the two-part margin
Indian F&O margin comes in two layers. The first and larger layer is **SPAN margin** (Standard Portfolio Analysis of Risk), a scenario engine the clearing corporation runs on your whole portfolio. It shocks the underlying up and down across a grid of price and volatility moves, reprices every position under each scenario, and charges you the **worst-case loss** the portfolio would suffer. For a single long future that worst case is simply a large adverse move in the index. The second layer is the **exposure margin** , a flat extra cushion (a small percentage of notional) stacked on top to cover gap risk that SPAN's grid might understate. Add them and you get the total margin blocked.
The numbers are not abstract. The OpenAlgo SDK exposes the broker's real margin calculator, so we can ask it exactly what one NIFTY lot costs to carry overnight:
EX 1The real SPAN plus exposure on one NIFTY lotNFOch58/01_margin_and_leverage.py
Copy
```
# One NIFTY future: notional, a rough SPAN band, and the REAL SPAN + exposure margin.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

SYM, EXCH, LOT = "NIFTY28JUL26FUT", "NFO", 65  # NIFTY lot size = 65

ltp = client.quotes(symbol=SYM, exchange=EXCH)["data"]["ltp"]
notional = ltp * LOT

# A rough eyeball band before asking the broker: index futures sit near ~11% of notional.
rough = 0.11 * notional

# The REAL number: SPAN (worst-case scan) + exposure margin, from the OpenAlgo margin API.
m = client.margin(positions=[{
    "symbol": SYM, "exchange": EXCH, "action": "BUY",
    "product": "NRML", "pricetype": "MARKET", "quantity": str(LOT), "price": "0",
}])["data"]
span, exp, total = m["span_margin"], m["exposure_margin"], m["total_margin_required"]

print(f"{SYM}  ({LOT} qty = 1 lot)")
print(f"Last price          : Rs {ltp:,.2f}")
print(f"Notional controlled : Rs {notional:,.0f}  (= {ltp:,.2f} x {LOT})")
print(f"Rough SPAN band     : Rs {rough:,.0f}  (~11% eyeball)")
print(f"SPAN margin (real)  : Rs {span:,.0f}")
print(f"Exposure margin     : Rs {exp:,.0f}")
print(f"Total margin        : Rs {total:,.0f}  ({total / notional * 100:.1f}% of notional)")
print(f"Implied leverage    : {notional / total:.2f}x")
print(f"\nOne NIFTY lot controls Rs {notional:,.0f} of index on Rs {total:,.0f} of margin "
      f"- {notional / total:.1f}x leverage.")
```

Live output

```
NIFTY28JUL26FUT  (65 qty = 1 lot)
Last price          : Rs 24,170.50
Notional controlled : Rs 1,571,082  (= 24,170.50 x 65)
Rough SPAN band     : Rs 172,819  (~11% eyeball)
SPAN margin (real)  : Rs 146,626
Exposure margin     : Rs 31,422
Total margin        : Rs 178,047  (11.3% of notional)
Implied leverage    : 8.82x

One NIFTY lot controls Rs 1,571,082 of index on Rs 178,047 of margin - 8.8x leverage.
```

For the July future at Rs 24,170.50, one lot of 65 is a notional of **Rs 1,571,082**. Against that the engine charges **Rs 146,626 of SPAN** plus **Rs 31,422 of exposure** , a total of **Rs 178,047** - about 11.3% of notional, an implied **leverage of 8.82x**. Notice our lazy eyeball band of 11% of notional (Rs 172,819) landed close to the real total, but only because index futures are well-behaved. Never trust the eyeball for a real position; the scenario engine is the source of truth, and it moves with volatility.
Rs 15.71 lakh notional controlled 1 NIFTY lot (65) 8.8x margin = 11% of notional SPAN Rs 1.47 L Exposure Rs 0.31 L = Total margin Rs 1.78 L You post SPAN plus exposure (about Rs 1.78 lakh) to control Rs 15.71 lakh of NIFTY - roughly 8.8x leverage
Key idea
Total F&O margin = **SPAN** (the clearing corporation's worst-case portfolio loss across a price and volatility grid) **+ exposure** (a flat notional cushion for gap risk). SPAN is portfolio-aware, so hedges reduce it; exposure is a blunt add-on. Both are set by the exchange and rise automatically when volatility rises.
## Collateral and haircuts
You do not have to fund margin entirely with cash. A quant book usually posts a mix of cash and **pledged securities** - shares, bonds or liquid funds held in your demat and pledged to the broker as **collateral**. The exchange does not value that collateral at full price; it applies a **haircut** , a discount that protects against the collateral itself falling. A liquid index ETF might carry a small haircut while a volatile mid-cap carries a steep one, so Rs 10 lakh of shares might support only Rs 8 lakh of margin. There is also a cash-equivalent rule: a portion of your margin (commonly around half) must be met with cash or cash-like instruments, because the exchange cannot settle daily mark-to-market losses in stock. Pledge a portfolio of pure equity and you will still be asked to keep real cash on hand for the daily flows.
Note
Haircuts, the cash-collateral ratio and the exact margin percentages are set and revised by the exchange and clearing corporation, not by your broker, and they change with market conditions. Treat any specific figure here as illustrative of the structure, and read the current circulars before you size a real book.
## Cross-margin and the leverage spectrum
Because SPAN reprices the **whole portfolio** under each scenario, offsetting positions earn a **cross-margin benefit** : a long future hedged with a short future in a correlated underlying, or a calendar spread across two expiries, loses far less in the worst case than either leg alone, so the margin can be a fraction of the gross. This is the structural reason hedged and spread strategies are capital-efficient and naked directional bets are not. It is also why leverage is not one number but a spectrum that depends on the instrument's own volatility. Compare an index future against a single-stock future:
EX 2Leverage across index and single-stock futuresNFOch58/02_leverage_bars.py
Copy
```
# Implied leverage (notional / total margin) for index vs single-stock futures, all real.
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

# (symbol, lot size, kind) - real NFO lot sizes.
book = [
    ("NIFTY28JUL26FUT", 65, "index"),
    ("BANKNIFTY28JUL26FUT", 30, "index"),
    ("RELIANCE28JUL26FUT", 500, "stock"),
    ("SBIN28JUL26FUT", 750, "stock"),
]

labels, levs, kinds = [], [], []
for sym, lot, kind in book:
    ltp = client.quotes(symbol=sym, exchange="NFO")["data"]["ltp"]
    total = client.margin(positions=[{
        "symbol": sym, "exchange": "NFO", "action": "BUY",
        "product": "NRML", "pricetype": "MARKET", "quantity": str(lot), "price": "0",
    }])["data"]["total_margin_required"]
    labels.append(sym.replace("28JUL26FUT", ""))
    levs.append(ltp * lot / total)
    kinds.append(kind)

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(7.2, 4.3))
palette = ["#7c83ff" if k == "index" else "#16a34a" for k in kinds]
sns.barplot(x=labels, y=levs, hue=labels, legend=False, palette=palette, ax=ax)
for i, v in enumerate(levs):
    ax.text(i, v + 0.08, f"{v:.1f}x", ha="center", fontsize=10)
ax.set_title("Implied leverage = notional / total margin (NRML, 1 lot)")
ax.set_ylabel("Leverage (x)")
ax.set_ylim(0, max(levs) + 1.2)
plt.savefig(Path(__file__).with_suffix(".png"), dpi=110, bbox_inches="tight")

idx = [l for l, k in zip(levs, kinds) if k == "index"]
stk = [l for l, k in zip(levs, kinds) if k == "stock"]
print("Implied leverage (notional / total margin), one lot each:")
for lab, lv in zip(labels, levs):
    print(f"  {lab:12s} {lv:.2f}x")
print(f"\nIndex futures ~{sum(idx) / len(idx):.1f}x vs single-stock futures "
      f"~{sum(stk) / len(stk):.1f}x - higher stock volatility means higher SPAN, so less leverage.")
```

Live output

```
Implied leverage (notional / total margin), one lot each:
  NIFTY        8.82x
  BANKNIFTY    8.73x
  RELIANCE     5.65x
  SBIN         5.68x

Index futures ~8.8x vs single-stock futures ~5.7x - higher stock volatility means higher SPAN, so less leverage.
```

![Leverage across index and single-stock futures chart](https://openalgo.in/quant/charts/ch58_02_leverage_bars.png)
The pattern is clean and economically honest. NIFTY sits at **8.82x** and BANKNIFTY at **8.73x** , while RELIANCE comes in at **5.65x** and SBIN at **5.68x**. A single stock is more volatile than a diversified index, so its SPAN scan finds a larger worst-case move, so the margin is a higher fraction of notional and the leverage is lower - roughly **8.8x for index futures versus 5.7x for single-stock futures**. The market is not rationing your ambition arbitrarily; it is charging risk for risk.
Tip
If a strategy is margin-hungry, look for a structural hedge before you look for more capital. Converting a naked short into a defined-risk spread, or pairing offsetting futures, can cut the SPAN charge sharply through cross-margining - often the cheapest "leverage" you will ever find, because it lowers genuine risk at the same time.
## Position limits and the ban period
Leverage has a ceiling that has nothing to do with your wallet. Every F&O underlying carries a **market-wide position limit (MWPL)** , a cap on the total open interest the whole market may hold in that name, plus **client-level limits** on any single participant. When aggregate open interest in a stock crosses 95% of its MWPL, the exchange puts the stock in a **ban period** : no new positions may be opened, and you may only reduce existing ones, until open interest falls back below 80%. For a quant this matters in two ways. First, it is a hard operational constraint - a signal that fires on a banned stock simply cannot be sized up, and trying generates rejects and penalties. Second, the ban list itself is information: a name jammed against its limit is crowded, and crowding is a risk and sometimes a signal, a theme we return to in the flow-based strategies of Module G.
## Physical settlement of stock F&O
Index derivatives settle in cash, but **single-stock F &O in India settles by physical delivery**. If you hold a stock futures or in-the-money options position into expiry, it does not vanish into a cash difference - it converts into an obligation to deliver or receive the actual shares. A long one-lot RELIANCE future taken to expiry becomes a purchase of 500 shares at the settlement price, demanding the full cash value, not the margin. The same applies to options that finish in the money, and there is a subtler trap: an option that is only marginally in the money can be **devolved** into a delivery obligation whose share value dwarfs the small premium you paid, which is why the exchange ramps up margins on stock F&O in the days before expiry.
Heads up
Never carry a single-stock F&O position into expiry unless you intend to take or give delivery and have the full cash or shares ready. The physical-settlement obligation is many times the margin you posted, and an in-the-money option you forgot about can devolve into a delivery you cannot fund. Close or roll stock contracts before expiry unless delivery is the plan.
## Margin as a constraint in a quant book
For a systematic book, margin is not an afterthought to a signal - it is part of the optimisation. Three facts make it binding. First, margin is dynamic: SPAN rises with volatility, so the exact day your positions move against you is the day the engine demands more, a pro-cyclical squeeze that can force deleveraging at the worst moment. Second, India enforces **peak margin** rules, sampling your intraday margin usage at random snapshots, so a strategy that briefly over-leverages between legs can incur penalties even if it ends the day square. Third, the daily **mark-to-market** settles your futures gains and losses in cash every evening, so a position can be solvent on paper yet still need cash to meet today's MTM. The practical discipline is to size to _available margin under stress_ , not to today's calm number: budget for SPAN inflating in a shock, keep the cash-equivalent portion funded, and treat the position limit and physical-settlement calendar as hard edges your code must respect.
That closes the derivatives module. We began with no-arbitrage forcing the synthetic future, the actual future and spot-plus-carry together, walked through the Greeks and the volatility risk premium priced off that forward, and now we end where every derivatives position truly lives - inside a margin account with limits, collateral and a settlement calendar. From here, Module G turns from the plumbing of instruments to the search for edge: building alpha signals that are worth posting all this margin to trade.
On this page
