Chapters
Module E · Strategy Playbook - Chapter 24
# Options Strategies
From the option chain to buying, spreads, straddles and hedging - all by symbol.
NFOINDEX
What you'll learn
  * ·Option chain & ATM
  * ·optionsymbol() & greeks
  * ·Buying calls / puts
  * ·Vertical & straddle legs
  * ·Hedging a position
  * ·Multi-leg orders


Options scare a lot of new traders, and the jargon is half the reason. Strikes, expiries, calls, puts, ATM, theta - it reads like a foreign language. But strip the vocabulary away and an option is a simple thing: **a contract that gives you the right, but not the obligation, to buy or sell something at a fixed price by a fixed date.** You pay a small premium for that right. That's it. Everything else is detail.
This chapter teaches options the way you'd actually trade them through code: discover what's available, read the chain, resolve the exact contract you want, understand how its price will move, and then place real (simulated) orders - single legs, spreads, straddles, and a hedge. We'll lean on a handful of purpose-built SDK calls that do the fiddly work for you, so you never have to guess a strike or hand-type a symbol.
Heads up
Options orders place positions. Before running a single order example, **confirm you are in analyze mode** - the flight simulator from Chapter 1 where orders are simulated and nothing real trades. Every order in this chapter was run that way. We'll check it explicitly in the first example, and you should make that a reflex.
## The two words that matter most: CE and PE
Indian options come in two flavours, and you'll see these suffixes on every symbol:
  * **CE - Call option.** The right to _buy_ the underlying at the strike. You buy a call when you think the price will **rise**.
  * **PE - Put option.** The right to _sell_ the underlying at the strike. You buy a put when you think the price will **fall**.


The **strike** is the fixed price written into the contract. The **expiry** is the date the contract dies. And every option is labelled by how its strike sits relative to the current market price:
  * **ATM (At The Money)** - strike closest to the current price. The most actively traded.
  * **ITM (In The Money)** - already has real value (a call with a strike _below_ the price; a put with a strike _above_).
  * **OTM (Out of The Money)** - pure hope value (a call _above_ the price; a put _below_). Cheaper, riskier.


Keep that map in your head and the rest of the chapter falls into place.
## Step zero: confirm the simulator is on
We never send an order without checking the mode first. `client.analyzerstatus()` tells us whether analyze mode is active. Make this the first thing your options scripts do.
EX 1Confirm analyze mode before tradingINDEXch24/01_confirm_analyze.py
Copy
```
# Safety first: never send an options order until analyze mode is confirmed ON.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

status = client.analyzerstatus()
mode = status["data"]["analyze_mode"]

print("Analyzer status:", status["data"])
if mode:
    print("\nAnalyze mode is ON -- option orders are SIMULATED. Safe to practise.")
else:
    print("\nWARNING: LIVE mode. Orders would hit the real exchange. Stop here.")
```

Live output

```
Analyzer status: {'analyze_mode': True, 'mode': 'analyze', 'total_logs': 457}

Analyze mode is ON -- option orders are SIMULATED. Safe to practise.
```

## Discovering a valid expiry
Here is the golden rule of options automation: **never hard-code an expiry date or a strike.** They go stale within days. Instead, ask the platform what's currently tradable. `client.expiry()` returns the live list of expiry dates for NIFTY options; we then keep the ones still in the future and pick the nearest.
There's one small format wrinkle. The expiry list comes back as `30-JUN-26`, but the option endpoints want the compact `30JUN26`. A two-line date conversion bridges the gap - and because it's all derived from today's date, this code keeps working forever.
EX 2Discover the nearest expiry at runtimeNFOch24/02_find_expiry.py
Copy
```
# Discover a valid expiry at runtime -- never hard-code dates that go stale.
import os
from datetime import datetime

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

resp = client.expiry(symbol="NIFTY", exchange="NFO", instrumenttype="options")
dates = resp["data"]  # e.g. ['23-JUN-26', '30-JUN-26', ...]
print("Expiries available:", dates[:5], "...")

# Keep only expiries strictly after today, then pick the nearest one.
today = datetime.now().date()
future = sorted(d for d in (datetime.strptime(x, "%d-%b-%y").date() for x in dates) if d > today)
nearest = future[0]
# Option endpoints want the compact DDMMMYY form, e.g. 30JUN26.
compact = nearest.strftime("%d%b%y").upper()

print("\nNearest future expiry:", nearest, "->", compact)
print("Days away            :", (nearest - today).days)
```

Live output

```
Expiries available: ['23-JUN-26', '30-JUN-26', '07-JUL-26', '14-JUL-26', '21-JUL-26'] ...

Nearest future expiry: 2026-06-30 -> 30JUN26
Days away            : 7
```

Key idea
This expiry-discovery snippet is the opening move of almost every example below. The pattern - fetch the list, drop past dates, take the nearest, reformat to `DDMMMYY` - is worth memorising. Discovered facts don't rot; hard-coded ones do.
## Reading the option chain
The **option chain** is the master table of an expiry: every strike, with its call on one side and its put on the other, plus live prices. `client.optionchain()` fetches it, and the `strike_count` parameter keeps it manageable by returning only a few strikes either side of the at-the-money price.
Each entry tells you the `strike`, an ATM/ITM/OTM `label`, and the `ltp` (last traded price, i.e. the premium) for both the CE and PE. Reading across a row, you can watch calls get cheaper and puts get dearer as the strike rises - the fundamental symmetry of the chain.
EX 3Fetch the chain and find ATMNFOINDEXch24/03_option_chain.py
Copy
```
# The option chain: every strike's CE and PE around the at-the-money price.
import os
from datetime import datetime

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# Discover the nearest expiry, then ask for 3 strikes either side of ATM.
dates = client.expiry(symbol="NIFTY", exchange="NFO", instrumenttype="options")["data"]
today = datetime.now().date()
nearest = sorted(d for d in (datetime.strptime(x, "%d-%b-%y").date() for x in dates) if d > today)[0]
expiry = nearest.strftime("%d%b%y").upper()

chain = client.optionchain(underlying="NIFTY", exchange="NSE_INDEX", expiry_date=expiry, strike_count=3)
print("Spot (underlying LTP):", chain["underlying_ltp"], "| ATM strike:", chain["atm_strike"])
print(f"\n{'Strike':>8} {'CE ltp':>8} {'CE lbl':>7} {'PE ltp':>8} {'PE lbl':>7}")
for row in chain["chain"]:
    ce, pe = row["ce"], row["pe"]
    print(f"{row['strike']:>8.0f} {ce['ltp']:>8} {ce['label']:>7} {pe['ltp']:>8} {pe['label']:>7}")
```

Live output

```
Spot (underlying LTP): 23824.1 | ATM strike: 23800.0

  Strike   CE ltp  CE lbl   PE ltp  PE lbl
   23650    262.9    ITM3       99    OTM3
   23700      233    ITM2   115.95    OTM2
   23750    203.6    ITM1      137    OTM1
   23800   173.35     ATM   159.45     ATM
   23850    150.2    OTM1    185.4    ITM1
   23900      127    OTM2    213.6    ITM2
   23950   107.95    OTM3   242.55    ITM3
```

Notice the `atm_strike` the server hands back. You don't have to compute it - the platform finds the strike nearest the current price for you.
## Resolving the exact symbol you want
Reading the chain is great for analysis, but to _trade_ you need the precise symbol - something like `NIFTY30JUN2623800CE`. Typing those by hand is how mistakes happen. `client.optionsymbol()` builds them for you: tell it the underlying, expiry, an **offset** (`ATM`, `ITM2`, `OTM3`, ...) and whether you want a `CE` or `PE`, and it returns the resolved symbol plus its lot size.
EX 4Resolve ATM / ITM / OTM symbolsNFOch24/04_option_symbol.py
Copy
```
# Resolve exact tradable symbols by offset: ATM / ITM / OTM, CE and PE.
import os
from datetime import datetime

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

dates = client.expiry(symbol="NIFTY", exchange="NFO", instrumenttype="options")["data"]
today = datetime.now().date()
nearest = sorted(d for d in (datetime.strptime(x, "%d-%b-%y").date() for x in dates) if d > today)[0]
expiry = nearest.strftime("%d%b%y").upper()


def resolve(offset, option_type):
    r = client.optionsymbol(underlying="NIFTY", exchange="NSE_INDEX",
                            expiry_date=expiry, offset=offset, option_type=option_type)
    return r["symbol"], r["lotsize"]


print("Expiry:", expiry)
for offset in ["ITM2", "ATM", "OTM2"]:
    ce_sym, lot = resolve(offset, "CE")
    pe_sym, _ = resolve(offset, "PE")
    print(f"{offset:>5}:  CE {ce_sym:<22} PE {pe_sym:<22} (lot {lot})")
```

Live output

```
Expiry: 30JUN26
 ITM2:  CE NIFTY30JUN2623700CE    PE NIFTY30JUN2623900PE    (lot 65)
  ATM:  CE NIFTY30JUN2623800CE    PE NIFTY30JUN2623800PE    (lot 65)
 OTM2:  CE NIFTY30JUN2623900CE    PE NIFTY30JUN2623700PE    (lot 65)
```

The offset is the clever part. `ATM` always means "nearest the money", `OTM2` means "two strikes out", and so on - relative to _today's_ price. So your code says what it _means_ ("two strikes out of the money") rather than a brittle number that's wrong tomorrow.
Tip
Each option trades in a fixed **lot size** - for NIFTY that's 65 units per lot. You can't buy a single unit; quantity must be a multiple of the lot size. `optionsymbol()` returns the current `lotsize` so you can size orders correctly without memorising it.
## The greeks: how an option's price moves
An option's premium isn't static - it breathes with the market, with time, and with fear. The **greeks** are five numbers that quantify exactly how. For a beginner, four of them matter:
  * **Delta** - how much the premium moves for a one-point move in the underlying. A delta of `0.5` means the option gains about half a point for every point NIFTY rises. ATM options sit near `0.5` (calls) or `-0.5` (puts).
  * **Gamma** - how fast delta itself changes. High gamma near ATM means your exposure shifts quickly.
  * **Theta** - **time decay** : the rupees an option _loses_ every day simply because expiry is closer. It's negative for buyers - the silent tax on holding options.
  * **Vega** - sensitivity to **implied volatility** (the market's expectation of future movement). When fear rises, vega-positive positions gain.


`client.optiongreeks()` computes all of these for any option symbol.
EX 5Delta, gamma, theta and vegaNFOch24/05_greeks.py
Copy
```
# The greeks: delta, gamma, theta, vega -- how an option's price will move.
import os
from datetime import datetime

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

dates = client.expiry(symbol="NIFTY", exchange="NFO", instrumenttype="options")["data"]
today = datetime.now().date()
nearest = sorted(d for d in (datetime.strptime(x, "%d-%b-%y").date() for x in dates) if d > today)[0]
expiry = nearest.strftime("%d%b%y").upper()

# Resolve the ATM call, then ask for its greeks.
sym = client.optionsymbol(underlying="NIFTY", exchange="NSE_INDEX",
                          expiry_date=expiry, offset="ATM", option_type="CE")["symbol"]
g = client.optiongreeks(symbol=sym, exchange="NFO", interest_rate=0.0,
                        underlying_symbol="NIFTY", underlying_exchange="NSE_INDEX")

print("Option        :", sym)
print("Days to expiry:", round(g["days_to_expiry"], 1))
print("Implied vol % :", g["implied_volatility"])
gk = g["greeks"]
print("\nDelta:", gk["delta"], " (price move per 1 pt of NIFTY)")
print("Gamma:", gk["gamma"], "(how fast delta changes)")
print("Theta:", gk["theta"], " (rupees lost to time decay per day)")
print("Vega :", gk["vega"], " (price move per 1% change in IV)")
```

Live output

```
Option        : NIFTY30JUN2623800CE
Days to expiry: 6.9
Implied vol % : 12.78

Delta: 0.5168  (price move per 1 pt of NIFTY)
Gamma: 0.000956 (how fast delta changes)
Theta: -12.1244  (rupees lost to time decay per day)
Vega : 13.0075  (price move per 1% change in IV)
```

Note
Theta is the single most important greek for an option _buyer_ to respect. Every day you hold, time decay nibbles at your premium - and it accelerates as expiry approaches. That's why buying far-out, near-expiry options and "hoping" is such a reliable way to lose money. The greeks turn that vague warning into a number you can see.
## Synthetic futures: the fair value hidden in the chain
Here's an elegant idea. Using just the ATM call and put, you can reconstruct what the future _should_ cost - the **synthetic future** - via put-call parity: `strike + call premium - put premium`. Comparing it to the spot price gives the **basis** , the cost of carry to expiry. `client.syntheticfuture()` does the arithmetic for you.
EX 6Build the synthetic future and basisNFOINDEXch24/06_synthetic_future.py
Copy
```
# Synthetic future: the future's fair value built from ATM call and put prices.
import os
from datetime import datetime

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

dates = client.expiry(symbol="NIFTY", exchange="NFO", instrumenttype="options")["data"]
today = datetime.now().date()
nearest = sorted(d for d in (datetime.strptime(x, "%d-%b-%y").date() for x in dates) if d > today)[0]
expiry = nearest.strftime("%d%b%y").upper()

sf = client.syntheticfuture(underlying="NIFTY", exchange="NSE_INDEX", expiry_date=expiry)
spot = sf["underlying_ltp"]
fair = sf["synthetic_future_price"]
basis = round(fair - spot, 2)

print("Expiry              :", sf["expiry"])
print("Spot (NIFTY index)  :", spot)
print("ATM strike          :", sf["atm_strike"])
print("Synthetic future    :", fair)
print("Basis (fair - spot) :", basis, "points")
print("\nBasis = the cost of carry to expiry; close to flat near expiry, and it")
print("can flip slightly negative once near-term carry and dividends net out.")
```

Live output

```
Expiry              : 30JUN26
Spot (NIFTY index)  : 23824.1
ATM strike          : 23800.0
Synthetic future    : 23813.9
Basis (fair - spot) : -10.2 points

Basis = the cost of carry to expiry; close to flat near expiry, and it
can flip slightly negative once near-term carry and dividends net out.
```

The basis is usually small - often slightly positive (the cost of carry), and it shrinks toward zero as expiry nears, sometimes dipping a touch negative once carry and dividends net out. A _wildly_ off basis is the interesting case: it can hint at mispricing - the seed of arbitrage strategies.
## Buying a call and a put
Now we trade. Buying an option is the simplest options position: your risk is capped at the premium you pay, and your upside is open. `client.optionsorder()` is purpose-built for this - you give it the offset and option type, and it resolves the strike and places the order in one call. We buy an ATM call (a bet up) and an ATM put (a bet down).
EX 7Buy a call and a putNFOch24/07_buy_call_put.py
Copy
```
# Buying options: a long call (bet up) and a long put (bet down), simulated.
import os
from datetime import datetime

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

dates = client.expiry(symbol="NIFTY", exchange="NFO", instrumenttype="options")["data"]
today = datetime.now().date()
nearest = sorted(d for d in (datetime.strptime(x, "%d-%b-%y").date() for x in dates) if d > today)[0]
expiry = nearest.strftime("%d%b%y").upper()

# offset resolves the strike for us; product NRML = carry (no intraday cutoff).
call = client.optionsorder(strategy="ch24", underlying="NIFTY", exchange="NSE_INDEX",
                           expiry_date=expiry, offset="ATM", option_type="CE", action="BUY",
                           quantity=65, pricetype="MARKET", product="NRML", splitsize=0)
put = client.optionsorder(strategy="ch24", underlying="NIFTY", exchange="NSE_INDEX",
                          expiry_date=expiry, offset="ATM", option_type="PE", action="BUY",
                          quantity=65, pricetype="MARKET", product="NRML", splitsize=0)

print("Bought CALL:", call["symbol"], "| status:", call["status"], "| id:", call["orderid"])
print("Bought PUT :", put["symbol"], "| status:", put["status"], "| id:", put["orderid"])
print("\nMode:", call.get("mode", "live"), "-- nothing real was traded.")
```

Live output

```
Bought CALL: NIFTY30JUN2623800CE | status: success | id: 26062354261953
Bought PUT : NIFTY30JUN2623800PE | status: success | id: 26062367624713

Mode: analyze -- nothing real was traded.
```

Tip
We use `product="NRML"` (the carry product for F&O) rather than `MIS` (intraday). `MIS` positions are force-closed at the daily square-off time, so an `MIS` order placed late in the session gets rejected. `NRML` carries the position and lets these examples run at any hour - a practical detail worth knowing.
## Multi-leg orders: spreads and straddles
Most real options strategies have more than one leg. Buying _and_ selling in a single coordinated order is what `client.optionsmultiorder()` is for - you hand it a list of legs and it places them together. Two classics:
A **vertical spread** (here a _bull call spread_) buys the ATM call and simultaneously sells a higher-strike call. Selling the upper call brings in premium that subsidises the one you bought, cutting your cost - at the price of capping your maximum gain. It's a defined-risk, defined-reward way to bet on a moderate rise.
EX 8A bull call spread in one orderNFOch24/08_vertical_spread.py
Copy
```
# A bull call spread: buy the ATM call, sell a higher call to cut the cost.
import os
from datetime import datetime

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

dates = client.expiry(symbol="NIFTY", exchange="NFO", instrumenttype="options")["data"]
today = datetime.now().date()
nearest = sorted(d for d in (datetime.strptime(x, "%d-%b-%y").date() for x in dates) if d > today)[0]
expiry = nearest.strftime("%d%b%y").upper()

# Two legs sent together. product NRML on each leg avoids intraday square-off.
resp = client.optionsmultiorder(
    strategy="ch24-bull-call", underlying="NIFTY", exchange="NSE_INDEX", expiry_date=expiry,
    legs=[
        {"offset": "ATM", "option_type": "CE", "action": "BUY", "quantity": 65, "product": "NRML"},
        {"offset": "OTM3", "option_type": "CE", "action": "SELL", "quantity": 65, "product": "NRML"},
    ],
)

print("Bull call spread on NIFTY", expiry, "| overall:", resp["status"])
for leg in resp["results"]:
    print(f"  leg {leg['leg']}: {leg['action']:<4} {leg['symbol']:<22} -> {leg['status']}")
```

Live output

```
Bull call spread on NIFTY 30JUN26 | overall: success
  leg 1: BUY  NIFTY30JUN2623800CE    -> success
  leg 2: SELL NIFTY30JUN2623950CE    -> success
```

A **long straddle** buys the ATM call _and_ the ATM put together. You don't care which way the market goes - you only need it to move _far_ , in either direction. Traders put on straddles ahead of big events (results, policy announcements) when a violent move looks likely but its direction is anyone's guess.
EX 9A long straddle in one orderNFOch24/09_straddle.py
Copy
```
# A long straddle: buy the ATM call AND the ATM put -- a bet on a big move.
import os
from datetime import datetime

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

dates = client.expiry(symbol="NIFTY", exchange="NFO", instrumenttype="options")["data"]
today = datetime.now().date()
nearest = sorted(d for d in (datetime.strptime(x, "%d-%b-%y").date() for x in dates) if d > today)[0]
expiry = nearest.strftime("%d%b%y").upper()

# Both legs at the same ATM strike, both BUY -- profits if NIFTY moves far either way.
resp = client.optionsmultiorder(
    strategy="ch24-straddle", underlying="NIFTY", exchange="NSE_INDEX", expiry_date=expiry,
    legs=[
        {"offset": "ATM", "option_type": "CE", "action": "BUY", "quantity": 65, "product": "NRML"},
        {"offset": "ATM", "option_type": "PE", "action": "BUY", "quantity": 65, "product": "NRML"},
    ],
)

print("Long straddle on NIFTY", expiry, "| overall:", resp["status"])
for leg in resp["results"]:
    print(f"  {leg['option_type']} leg: BUY {leg['symbol']:<22} -> {leg['status']}")
print("\nMax loss is the combined premium; profit grows once price moves past it.")
```

Live output

```
Long straddle on NIFTY 30JUN26 | overall: success
  CE leg: BUY NIFTY30JUN2623800CE    -> success
  PE leg: BUY NIFTY30JUN2623800PE    -> success

Max loss is the combined premium; profit grows once price moves past it.
```

Key idea
With `optionsmultiorder`, set `product` on **each leg** (we use `NRML`). A top-level product is not reliably applied to the legs, so make it explicit per leg. Each leg in the response reports its own status, so always loop the `results` and check every leg succeeded.
## Hedging: the protective put
Options aren't only for speculating - they're insurance. A **protective put** pairs a bullish position (here, a long ATM call standing in for owning the underlying) with a far out-of-the-money put. That put does nothing while the market rises, but if the market collapses, it gains value and **caps your loss** below its strike. You pay a premium for the protection, exactly like an insurance excess.
EX 10Hedge with a protective putNFOch24/10_protective_put.py
Copy
```
# Hedging: own the future's upside but cap the downside by buying a put.
import os
from datetime import datetime

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

dates = client.expiry(symbol="NIFTY", exchange="NFO", instrumenttype="options")["data"]
today = datetime.now().date()
nearest = sorted(d for d in (datetime.strptime(x, "%d-%b-%y").date() for x in dates) if d > today)[0]
expiry = nearest.strftime("%d%b%y").upper()

# Synthetic-long via a call, protected by an OTM put -- the put is the insurance.
resp = client.optionsmultiorder(
    strategy="ch24-protective-put", underlying="NIFTY", exchange="NSE_INDEX", expiry_date=expiry,
    legs=[
        {"offset": "ATM", "option_type": "CE", "action": "BUY", "quantity": 65, "product": "NRML"},
        {"offset": "OTM5", "option_type": "PE", "action": "BUY", "quantity": 65, "product": "NRML"},
    ],
)

print("Protected long on NIFTY", expiry, "| overall:", resp["status"])
for leg in resp["results"]:
    role = "upside (long call)" if leg["option_type"] == "CE" else "insurance (long put)"
    print(f"  {leg['symbol']:<22} {leg['action']:<4} -> {leg['status']:<8} {role}")
print("\nThe OTM put caps your loss below its strike, for the cost of its premium.")
```

Live output

```
Protected long on NIFTY 30JUN26 | overall: success
  NIFTY30JUN2623800CE    BUY  -> success  upside (long call)
  NIFTY30JUN2623550PE    BUY  -> success  insurance (long put)

The OTM put caps your loss below its strike, for the cost of its premium.
```

This is the mindset shift that separates gamblers from risk managers: the put isn't there to make money, it's there so that a single bad day can't ruin you.
## Try it yourself
  * Change the spread in the bull-call example to a wider `OTM5` short leg. The cost rises, but so does the maximum profit - inspect both legs in the output.
  * Pull the greeks for an `OTM3` call and compare its delta and theta to the ATM call. Notice how much lower the delta is.
  * Build a _short_ straddle by switching both legs to `SELL` (this collects premium and profits if the market stays _still_) - and think hard about why its risk profile is the dangerous mirror image of the long straddle.


## Recap
  * An option is a _right, not an obligation_ : **CE** (call) bets up, **PE** (put) bets down; **ATM/ITM/OTM** describe the strike versus the price.
  * Always **confirm analyze mode** before placing any options order.
  * **Never hard-code** expiries or strikes - discover them with `client.expiry()`, `client.optionchain()`, and `client.optionsymbol()`.
  * The **greeks** (delta, gamma, theta, vega) tell you how a premium will move; theta, the time-decay tax, matters most to buyers.
  * `client.syntheticfuture()` reconstructs fair value from the ATM call and put.
  * `client.optionsorder()` places a single leg; `client.optionsmultiorder()` places spreads, straddles and hedges - set `product` on every leg and check each leg's status.
  * A **protective put** is insurance: it caps the downside of a bullish position for the cost of a premium.


Next we move from options to the full execution toolkit - every order type, smart and basket and split orders, modifications and cancellations - the plumbing that turns a strategy into live trades.
On this page
