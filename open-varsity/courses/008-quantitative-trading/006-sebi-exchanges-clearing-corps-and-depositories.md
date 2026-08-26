Chapters
Module A · Quant Career Map & Indian Market Structure - Chapter 06
# SEBI, Exchanges, Clearing Corps and Depositories
The institutional plumbing - the regulator, the exchanges, the clearing corporations with their default waterfall, the depositories, and interoperability.
NSE
What you'll learn
  * ·SEBI's mandate
  * ·Exchanges vs clearing corporations
  * ·The CCP and default waterfall
  * ·NSDL and CDSL depositories
  * ·Clearing interoperability
  * ·Why the plumbing matters to a quant


You click **buy** on 100 shares of Reliance. A number flickers, the order fills, and you move on. But behind that one click, a remarkable machine spins up - a regulator, two exchanges, a clearing corporation that briefly _becomes_ your counterparty, two depositories, and your bank - all coordinating to make sure that in 24 hours you actually own the shares and the seller actually has the money. A quant who doesn't understand this plumbing will misprice carry, misjudge risk, and be baffled when a "holding" behaves differently from a "position." Let's open the panel.
## Who's who
Four kinds of institution stand behind every Indian trade:
  * **SEBI** - the regulator. It writes the rules, licenses the players, and runs surveillance. When you read about lot-size changes, F&O curbs or new settlement cycles, that's SEBI.
  * **Exchanges (NSE, BSE)** - the marketplaces where orders meet and a price is discovered. They match buyers and sellers; they do _not_ hold your money.
  * **Clearing corporations (NSE Clearing, Indian Clearing Corp)** - the unsung hero. After a match, the clearing corp steps in between buyer and seller and _guarantees_ the trade. Even if the other side defaults, you're made whole.
  * **Depositories (NSDL, CDSL)** - the digital vaults where your shares actually live, in your demat account.


## The life of a trade
Here's what your one click actually triggers:
Your order Exchange match Clearing corp guarantees it Settle T+1 Demat + cash change hands One click, five steps - and a guarantee in the middle
The magic is step three. The moment the clearing corporation **novates** the trade - legally inserting itself as buyer to every seller and seller to every buyer - you stop worrying about who's on the other side. That guarantee is _why_ you can trade an anonymous order book without fear, and it's funded by the margins every participant posts. No clearing corp, no modern market.
Key idea
The exchange finds the price; the **clearing corporation guarantees the trade**. That separation - price discovery from counterparty risk - is the quiet foundation that lets millions of strangers trade safely every second.
## T+1, and the road to T+0
When does the money and stock actually move? In India, **T+1** : trade today, settle tomorrow. That sounds mundane, but India is genuinely _ahead of the world_ here - the US only moved to T+1 in 2024, and India did it first, then went further by launching an optional **T+0** (same-day) settlement for a set of stocks.
Why a quant cares:
  * **Capital efficiency.** Faster settlement frees up your capital sooner - it can be redeployed rather than locked in a pending trade.
  * **Overnight risk.** A delivery trade carries risk until it settles; shorter cycles shrink that window.
  * **Arbitrage.** Settlement timing creates funding and basis effects that cash-futures arbitrage (Module G) lives on.


The capital that flows through all this machinery is something you can read straight from the SDK - your funds, the cash that clearing actually moves:
EX 1The capital settlement movesNSEch06/01_settled_capital.py
Copy
```
# The capital the settlement system moves - your funds, settled and available to trade.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

data = client.funds()["data"]
print(f"Available cash : {float(data['availablecash']):>14,.2f}")
print(f"Utilised       : {float(data['utiliseddebits']):>14,.2f}")
print(f"Realised P&L   : {float(data.get('m2mrealized', 0)):>14,.2f}")
print(f"Collateral     : {float(data.get('collateral', 0)):>14,.2f}")
print("\nThis cash is exactly what flows through clearing and settles to/from your bank on T+1.")
print("A quant tracks settled vs available capital - it decides how much can actually be deployed.")
```

Live output

```
Available cash :  10,000,000.00
Utilised       :           0.00
Realised P&L   :           0.00
Collateral     :           0.00

This cash is exactly what flows through clearing and settles to/from your bank on T+1.
A quant tracks settled vs available capital - it decides how much can actually be deployed.
```

That available-cash figure is what gets debited when you buy and credited when you sell, settling to and from your bank on the T+1 cycle. A quant watches the gap between _settled_ and _available_ capital, because it decides how much can genuinely be deployed today.
## Positions vs holdings - the same plumbing, felt directly
Here's where the plumbing becomes concrete in your own code. When you buy intraday and square off the same day, nothing settles - that's a **position** , and it vanishes at the close. When you buy for delivery, it settles through the cycle above and becomes a **holding** sitting in your demat. Same symbol, completely different life - and your strategy must know which it's running. A quant treats "intraday position" and "settled holding" as different instruments with different risks, costs and funding.
## Try it yourself
  * Look up SEBI's current settlement circular. Which stocks are in the T+0 pilot today, and how is the list growing?
  * Think through a short delivery: if a seller fails to deliver shares, what does the clearing corporation do? (Hint: auction.) Why does that protect you as the buyer?
  * List one way a shorter settlement cycle changes the economics of a cash-futures arbitrage. We'll formalise it in Module G.


## Recap
  * Every trade involves four players: **SEBI** (rules), **exchanges** (price discovery), **clearing corporations** (the guarantee), and **depositories** (your shares).
  * The clearing corp **novates** the trade - becoming counterparty to both sides - so you never bear the risk of an anonymous stranger defaulting.
  * India settles **T+1** (ahead of most of the world) and is rolling out optional **T+0** - which improves capital efficiency and shrinks overnight risk.
  * A square-off-by-close **position** and a settled **holding** are different animals; quant code must track which is which.


With the field mapped and the plumbing understood, one force still quietly decides whether any strategy survives: cost. Next we build the all-in cost model - STT, brokerage, charges, GST - that turns paper edges into real, or imaginary, profits.
On this page
