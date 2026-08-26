Chapters
Module I · Going Live - Chapter 32
# Risk & Position Sizing
Turn a signal into the right quantity - sizing by fixed-fractional risk, the stop distance, ATR and portfolio heat, with a reusable lot-aware sizer.
NSENFOMCX
What you'll learn
  * ·Why sizing beats entries
  * ·Fixed-fractional: risk 1% per trade
  * ·Quantity from the stop distance
  * ·ATR-based stops & volatility sizing
  * ·Portfolio heat & exposure caps
  * ·A reusable position_size() helper


In the last chapter you learned to _manage_ a live trade - stop-loss, target, trailing stop. But we skipped the question that comes first: **how many shares did you buy in the first place?** Get that number wrong and the finest exit logic in the world won't save you. Buy too much and a single ordinary loss craters your account; buy too little and even a great strategy barely moves the needle.
This is position sizing, and it's the most under-taught, over-important skill in trading. The good news: it's just arithmetic, and the SDK hands you everything you need - your capital, live prices, and volatility. Let's turn "I have a signal" into "I buy exactly this many."
## Why size is the decision that keeps you alive
Two traders run the **same** strategy with the same 55% win rate. One risks 2% of capital per trade; the other risks 20% because a few big wins felt good. After a normal losing streak - which every strategy has - the first trader is down a bit and still playing. The second is wiped out and can never recover, because a 50% loss needs a 100% gain just to get back to even.
That asymmetry is the whole game. Sizing decides how long you survive your inevitable bad runs, and only survivors are around when the good runs come.
Key idea
Your edge earns money slowly; bad sizing loses it instantly. **Decide your risk per trade before your entry, and never let a single trade threaten your ability to place the next one.**
## Risk a fixed fraction, never a fixed quantity
Beginners size in shares - _"I'll buy 100 of everything."_ But 100 shares of a 3000-rupee stock is thirty times the exposure of 100 shares of a 100-rupee stock. The professional unit isn't shares, it's **risk** : a fixed, small percentage of your capital you're willing to lose if the trade goes against you. One percent is a sane default.
Read your real capital straight from the account and turn it into a rupee budget:
EX 1Risk a fixed 1% of capitalNSEch32/01_risk_per_trade.py
Copy
```
# The first rule of sizing: decide how much you can LOSE before how much you can buy.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

RISK_PCT = 1.0          # risk at most 1% of capital on any single trade

capital = float(client.funds()["data"]["availablecash"])
risk_amount = capital * RISK_PCT / 100

print(f"Available capital : {capital:>13,.2f}")
print(f"Risk per trade    : {RISK_PCT:.1f}%  ->  {risk_amount:>10,.2f} rupees")
print("\nThat rupee figure - not a share count - is the real budget for one trade.")
```

Notice what we computed: not a share count, but a **rupee amount you can afford to lose**. Every sizing method in this chapter starts here and works backwards to a quantity.
## From rupee risk to a share count
Here's the formula that does all the work. If your stop-loss is a known distance below your entry, then each share can lose you `entry - stop` rupees. Divide your risk budget by that per-share risk and you get your quantity:
> **quantity = risk budget / (entry - stop)**
EX 2Quantity from the stop distanceNSEch32/02_size_from_stop.py
Copy
```
# Turn a rupee risk budget into a share quantity using the distance to your stop.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

RISK_PCT = 1.0
SYMBOL, EXCHANGE = "RELIANCE", "NSE"

capital = float(client.funds()["data"]["availablecash"])
risk_amount = capital * RISK_PCT / 100

entry = client.quotes(symbol=SYMBOL, exchange=EXCHANGE)["data"]["ltp"]
stop = entry * 0.98                        # a 2% stop, for illustration
risk_per_share = entry - stop

qty = int(risk_amount // risk_per_share)    # whole shares only, always round down

print(f"Entry        : {entry:.2f}")
print(f"Stop         : {stop:.2f}   (risk/share = {risk_per_share:.2f})")
print(f"Risk budget  : {risk_amount:,.2f}")
print(f"-> Quantity  : {qty}   (worst-case loss if stopped = {qty * risk_per_share:,.2f})")
print("\nWiden the stop and the quantity shrinks - risk stays pinned to your budget.")
```

The beauty of this is self-correcting: a wider stop makes `entry - stop` bigger, so the quantity automatically shrinks to keep your rupee risk constant. You never have to guess - the stop _is_ the size.
Heads up
Always round the quantity **down** , never up. Rounding up nudges you over your risk limit on every trade, and those little overshoots compound into a real problem. `//` (floor division) does this for you.
## Let volatility set the stop - and the size
A fixed 2% stop is arbitrary. A calm stock barely moves 2% in a week; a wild one blows through it before lunch. Back in Chapter 13 you met **ATR** - the average true range, the typical distance price travels in a bar. Place your stop a multiple of ATR away and it adapts to each instrument's real behaviour. Then size off that ATR-based stop distance:
EX 3ATR-based stop and sizeNSEch32/03_atr_position_size.py
Copy
```
# A volatility-aware stop: place it 2 x ATR away, then size off that distance.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

RISK_PCT = 1.0
ATR_MULT = 2.0
SYMBOL, EXCHANGE = "RELIANCE", "NSE"

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=250)).strftime("%Y-%m-%d")
df = client.history(symbol=SYMBOL, exchange=EXCHANGE, interval="D", start_date=start, end_date=end)

entry = df["close"].iloc[-1]
atr = ta.atr(df["high"], df["low"], df["close"], 14).iloc[-1]
stop_distance = ATR_MULT * atr

capital = float(client.funds()["data"]["availablecash"])
risk_amount = capital * RISK_PCT / 100
qty = int(risk_amount // stop_distance)

print(f"{SYMBOL}: entry {entry:.2f}   ATR(14) {atr:.2f}")
print(f"Stop {ATR_MULT:.0f}xATR away -> {entry - stop_distance:.2f}   (risk/share {stop_distance:.2f})")
print(f"Risk budget {risk_amount:,.2f}  ->  quantity {qty}")
print("\nCalm stock -> tight ATR -> bigger size; wild stock -> smaller size, same rupee risk.")
```

This single idea quietly solves a hard problem: it lets you trade a sleepy large-cap and a jumpy commodity with the _same_ rupee risk, because the volatile one automatically gets a smaller position.
## Same risk on every name: volatility targeting
Scale that up to a whole watchlist and you get **volatility targeting** - sizing each position so they all carry roughly equal risk. The low-volatility names get more units, the high-volatility names get fewer, and no single position dominates your fortunes:
EX 4Equal risk across a watchlistNSEMCXch32/04_volatility_target.py
Copy
```
# Volatility targeting: give every position the SAME rupee risk, whatever its vol.
import os
from datetime import datetime, timedelta

from openalgo import api, ta

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

RISK_PER_NAME = 5000.0       # target rupee risk for each holding
WATCHLIST = [("RELIANCE", "NSE"), ("TATASTEEL", "NSE"), ("GOLDM03JUL26FUT", "MCX")]

end = datetime.now().strftime("%Y-%m-%d")
start = (datetime.now() - timedelta(days=200)).strftime("%Y-%m-%d")

print(f"{'SYMBOL':18s}{'PRICE':>10s}{'ATR':>9s}{'QTY':>7s}{'RISK':>12s}")
for sym, exch in WATCHLIST:
    df = client.history(symbol=sym, exchange=exch, interval="D", start_date=start, end_date=end)
    price = df["close"].iloc[-1]
    atr = ta.atr(df["high"], df["low"], df["close"], 14).iloc[-1]
    qty = int(RISK_PER_NAME // (2 * atr))      # 2 x ATR stop distance
    print(f"{sym:18s}{price:>10.2f}{atr:>9.2f}{qty:>7d}{qty * 2 * atr:>12,.2f}")

print(f"\nEach line risks about {RISK_PER_NAME:,.0f} - the volatile names just get fewer units.")
```

Run it and look at the `QTY` column swing wildly while the `RISK` column stays flat. That flat risk column is the entire point - a portfolio where every holding gets an equal vote, not where your most volatile pick quietly runs the show.
## Portfolio heat: cap your total exposure
Sizing each trade safely isn't enough if you hold twenty of them at once. The sum of all your open risk is your **portfolio heat** , and it's what a bad _day_ - not a bad trade - can cost you. Add a ceiling (say 6% of capital) and refuse new trades that would breach it:
EX 5Cap total open riskNSEch32/05_portfolio_heat.py
Copy
```
# Portfolio heat: the TOTAL risk across all open trades - cap it, or one bad day stings.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

MAX_HEAT_PCT = 6.0       # never have more than 6% of capital at risk at once

capital = float(client.funds()["data"]["availablecash"])

# Each open position as (symbol, quantity, entry, stop)
open_positions = [
    ("RELIANCE", 40, 1400.0, 1372.0),
    ("INFY", 30, 1550.0, 1520.0),
    ("TATASTEEL", 200, 150.0, 146.0),
]

heat = 0.0
for sym, qty, entry, stop in open_positions:
    risk = qty * (entry - stop)
    heat += risk
    print(f"{sym:12s} risk {risk:>10,.2f}  ({risk / capital * 100:.2f}% of capital)")

heat_pct = heat / capital * 100
print(f"\nTotal open risk (heat): {heat:,.2f}  =  {heat_pct:.2f}% of capital")
if heat_pct > MAX_HEAT_PCT:
    print(f"OVER the {MAX_HEAT_PCT:.0f}% limit - trim or close a position before adding another.")
else:
    print(f"Within the {MAX_HEAT_PCT:.0f}% limit - room for {MAX_HEAT_PCT - heat_pct:.2f}% more risk.")
```

Note
Heat matters most when your positions are correlated. Five bank stocks sized at 1% each aren't five independent 1% bets - on a bad day for banks they move together, closer to one 5% bet. When in doubt, treat a correlated cluster as a single position and size the group, not each name.
## A reusable position sizer
Let's bottle all of this into one helper you can drop into any strategy. It takes capital, your risk percentage, the entry and stop, and a **lot size** - because futures and options trade in fixed lots (remember NIFTY's lot of 65 from Chapter 3), so the quantity must round to whole lots, not arbitrary units:
EX 6A reusable position_size() helperNSENFOch32/06_position_sizer.py
Copy
```
# A reusable sizer: rupee risk in, whole-lot quantity out - safe for F&O.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)


def position_size(capital, risk_pct, entry, stop, lot_size=1):
    """Whole-lot quantity that risks at most risk_pct of capital down to the stop."""
    per_unit = abs(entry - stop)
    if per_unit == 0:
        return 0
    risk_amount = capital * risk_pct / 100
    units = risk_amount // per_unit
    lots = int(units // lot_size)            # round DOWN to whole lots
    return lots * lot_size


capital = float(client.funds()["data"]["availablecash"])

# Equity: 1 share = 1 unit
eq = position_size(capital, 1.0, entry=1400, stop=1372, lot_size=1)
print(f"RELIANCE equity   -> qty {eq}   (risk {eq * 28:,.2f})")

# Futures must trade in lots (NIFTY lot = 65 from Chapter 3)
fut = position_size(capital, 1.0, entry=25900, stop=25750, lot_size=65)
print(f"NIFTY fut lot=65  -> qty {fut}   ({fut // 65} lot/s, risk {fut * 150:,.2f})")
print("\nSame 1% rule everywhere - the lot rounding just keeps F&O orders valid.")
```

That one function is the bridge between every strategy you've built and a real order: signal in, _correctly sized_ quantity out. Wire it in front of the `placeorder()` call from Chapter 25 and the trade manager from Chapter 31, and you have the full loop - decide size, place the order, manage the exit.
## Try it yourself
  * Change `RISK_PCT` from 1.0 to 0.5 and watch every quantity halve. That's how you dial total aggression with a single number.
  * Feed `position_size()` a tiny stop distance and a huge one. Confirm the rupee risk stays fixed while the quantity moves inversely.
  * Add a `max_capital_pct` guard to the sizer so a very tight stop can't tell you to buy more than, say, 25% of capital in one name.
  * Combine this with Chapter 18's scanner: size every hit, then sort by quantity to see where your risk budget naturally concentrates.


## Recap
  * Size in **risk** , not shares: pick a small fixed fraction of capital (1% is a sane default) to lose per trade, read your real capital from `funds()`.
  * **quantity = risk budget / (entry - stop)** - and always round _down_.
  * Let **ATR** set the stop distance so size adapts to each instrument's volatility; extend that to **volatility targeting** for equal risk across a watchlist.
  * Track **portfolio heat** - the sum of all open risk - and cap it, remembering correlated names move as one.
  * A single `position_size()` helper with a `lot_size` argument turns any signal into a correctly sized, F&O-valid order.


You've now closed the loop. From your first `quotes()` call to indicators, signals, backtests, machine learning, a live WebSocket feed, and finally the risk discipline that ties it all together - you have every piece of a real, survivable trading system. Size small, trade in analyze mode first, and let the maths - not the mood - decide.
On this page
