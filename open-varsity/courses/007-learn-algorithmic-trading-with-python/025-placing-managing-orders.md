Chapters
Module F · Execution - Chapter 25
# Placing & Managing Orders
Every order type - market, limit, SL, smart, basket, split - plus modify and cancel.
NSENFOMCX
What you'll learn
  * ·placeorder() types
  * ·placesmartorder()
  * ·basket & split orders
  * ·modify / cancel
  * ·Order & position books
  * ·Close all positions


Up to now you've been a spectator: pulling quotes, charting history, building signals. This is the chapter where you finally pick up the remote control and _act_. Placing an order is the moment a strategy stops being an idea on a screen and becomes a position in the market - and it's also the moment mistakes start costing money. So we're going to be careful, methodical, and we're going to do every single thing in **analyze mode** , where orders are simulated and nothing actually trades.
By the end you'll know how to send every order type the SDK supports - market, limit, stop-loss, smart, basket and split - how to modify and cancel them, how to read back what happened from your order, trade and position books, and how to flatten everything with a single call. These are the exact building blocks every bot in the rest of the series uses to execute.
Heads up
Everything below was run on a server in **analyze mode** , so the responses are realistic but simulated. Before you ever run order code yourself, confirm the mode - the very first example does exactly that. Going live should be a deliberate choice, never an accident.
## Always check the mode first
A professional pilot runs a pre-flight checklist before every takeoff. Yours is one line: _am I in analyze mode or live mode?_ `client.analyzerstatus()` answers it. Get into the habit of running this before any order session - it's the cheapest insurance you'll ever buy.
EX 1Confirm you are in analyze modech25/01_confirm_analyze.py
Copy
```
# Before placing any order, confirm the server is in analyze mode (simulated).
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

status = client.analyzerstatus()
data = status["data"]

print(f"Mode        : {data['mode']}")
print(f"Analyze mode: {data['analyze_mode']}")

if data["analyze_mode"]:
    print("Safe to practise: every order below is simulated, nothing trades.")
else:
    print("WARNING: live mode is on. Orders would hit the real exchange.")
```

Live output

```
Mode        : analyze
Analyze mode: True
Safe to practise: every order below is simulated, nothing trades.
```

## The anatomy of an order
Every order you place answers the same handful of questions. Learn these five and you can place anything:
  * **symbol** and **exchange** - _what_ you're trading and _where_ (`RELIANCE` on `NSE`, `GOLDM03JUL26FUT` on `MCX`).
  * **action** - `BUY` or `SELL`.
  * **price_type** - _how_ you want to be filled: `MARKET`, `LIMIT`, `SL`, or `SL-M`.
  * **product** - _what kind_ of position: `CNC` (delivery - you hold the shares), `NRML` (futures & options carried overnight), or `MIS` (intraday, auto-squared-off the same day).
  * **quantity** - how many shares or how many units (for F&O, a whole number of the lot size).


Key idea
In the OpenAlgo Python SDK, `placeorder`, `placesmartorder` and `splitorder` all take the price type as `price_type=` (with the underscore). The exception is `basketorder`: each leg is a dictionary that uses the key `pricetype` (no underscore) instead - a small inconsistency that trips people up, so watch for it. Across the platform: products are `CNC` / `NRML` / `MIS`, actions are `BUY` / `SELL`, and price types are `MARKET` / `LIMIT` / `SL` / `SL-M`.
## Market orders: fill me now
A **market order** says "I don't care about the exact price, just get me in (or out) right now." It fills almost instantly at whatever price the market is offering. It's the right tool when _being in the trade_ matters more than _the exact price_ - for example, exiting a losing position fast. The response hands you back an **order id** (your receipt) and a **status**.
EX 2Place a MARKET orderNSEch25/02_market_order.py
Copy
```
# A MARKET order: buy 1 RELIANCE for delivery (CNC) at the best available price.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# price_type=MARKET means "fill me now at whatever the market is".
# product=CNC means delivery (you intend to hold the shares).
response = client.placeorder(
    strategy="Chapter25",
    symbol="RELIANCE",
    exchange="NSE",
    action="BUY",
    price_type="MARKET",
    product="CNC",
    quantity=1,
)

print(response)
print(f"Status : {response['status']}")
print(f"Order id: {response.get('orderid')}")
```

Live output

```
{'mode': 'analyze', 'orderid': '26062323464338', 'status': 'success'}
Status : success
Order id: 26062323464338
```

Tip
NSE and BSE equities stop trading at 15:30 IST, and `MIS` (intraday) orders are rejected after the broker's square-off time. That's why this example uses `CNC` (delivery). When you want to practise intraday-style orders in the evening, switch to an `MCX` commodity - those trade well into the night.
## Limit orders: fill me at my price or better
A **limit order** sets the worst price you'll accept. A BUY limit at 700 means "buy, but never pay more than 700." If the market is above your price, the order simply _rests_ as pending until the market comes to you (or you cancel it). Limits give you price control at the cost of certainty - you might never get filled.
EX 3Place a LIMIT orderNSEch25/03_limit_order.py
Copy
```
# A LIMIT order: buy SBIN only if the price reaches your chosen level or better.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# A LIMIT order needs a price. We bid below the market so it rests as a pending
# order instead of filling instantly. trigger_price is 0 (not a stop order).
response = client.placeorder(
    strategy="Chapter25",
    symbol="SBIN",
    exchange="NSE",
    action="BUY",
    price_type="LIMIT",
    product="CNC",
    quantity=1,
    price=700,
    trigger_price=0,
)

print(f"Status : {response['status']}")
print(f"Order id: {response.get('orderid')}  (resting at 700)")
```

Live output

```
Status : success
Order id: 26062385309963  (resting at 700)
```

## Stop orders: protect the downside
This is the order type that keeps you in business. A **stop order** sits dormant until the price hits a **trigger** , then springs to life to get you out of a trade that's going wrong.
  * **SL (Stop-Loss Limit)** - when the trigger is hit, a _limit_ order is sent. You control the price but risk not filling in a fast move.
  * **SL-M (Stop-Loss Market)** - when the trigger is hit, a _market_ order is sent. Guaranteed to fill, but at whatever price is available.


Here we attach both to F&O positions: an `SL` on a NIFTY future and an `SL-M` on a gold future.
EX 4SL and SL-M stop ordersNFOMCXch25/04_stop_loss_orders.py
Copy
```
# Stop orders that protect a position: SL (stop-limit) and SL-M (stop-market).
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# SL = Stop-Loss LIMIT. When price hits trigger_price (24820), a SELL LIMIT at
# price (24800) is sent. Use on an NFO future (NRML = overnight carry).
sl = client.placeorder(
    strategy="Chapter25", symbol="NIFTY30JUN26FUT", exchange="NFO",
    action="SELL", price_type="SL", product="NRML",
    quantity=65, price=24800, trigger_price=24820,
)
print(f"SL   order id: {sl.get('orderid')}  status: {sl['status']}")

# SL-M = Stop-Loss MARKET. Only a trigger is needed; once hit it fills at market.
slm = client.placeorder(
    strategy="Chapter25", symbol="GOLDM03JUL26FUT", exchange="MCX",
    action="SELL", price_type="SL-M", product="NRML",
    quantity=1, trigger_price=140000,
)
print(f"SL-M order id: {slm.get('orderid')}  status: {slm['status']}")
```

Live output

```
SL   order id: 26062344429557  status: success
SL-M order id: 26062352256073  status: success
```

Note
Remember the price rules. `MARKET`: no price needed. `LIMIT`: needs a `price`. `SL`: needs _both_ a `price` (the limit) and a `trigger_price`. `SL-M`: needs only a `trigger_price`.
## Smart orders: trade to a target, not a quantity
Here's a subtle but powerful idea. A normal order adds a fixed quantity. A **smart order** (`placesmartorder`) instead drives your position to an _absolute target size_ you specify with `position_size`. OpenAlgo looks at what you currently hold and sends only the difference.
Why does that matter? Because bots fire repeatedly. If your signal says "be long 5 lots" and you're already long 3, a smart order quietly buys just 2 more - it never doubles you up by mistake. Set `position_size=0` and it flattens you. It's the cleanest way to keep a live position exactly where your strategy wants it.
EX 5Place a smart order to a target sizeNSEch25/05_smart_order.py
Copy
```
# placesmartorder() drives your position to a TARGET size, not a fixed quantity.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# position_size is the absolute target holding you want to end up with.
# OpenAlgo checks your current position and only sends the difference.
# Here: target 5 long. If you hold 0, it buys 5; if you hold 3, it buys 2.
response = client.placesmartorder(
    strategy="Chapter25",
    symbol="RELIANCE",
    exchange="NSE",
    action="BUY",
    price_type="MARKET",
    product="CNC",
    quantity=1,
    position_size=5,
)

print(f"Status  : {response['status']}")
print(f"Order id: {response.get('orderid')}")
print("Smart orders keep you AT a target size instead of adding blindly.")
```

Live output

```
Status  : success
Order id: 26062320063210
Smart orders keep you AT a target size instead of adding blindly.
```

## Basket orders: many orders, one call
A **basket order** fires a whole list of different orders in a single request. Perfect for a pairs trade (long one stock, short another), or for entering a multi-stock portfolio at once. Each item in the list is its own little dictionary with the same fields you already know.
EX 6Fire a basket of ordersNSEch25/06_basket_order.py
Copy
```
# A basket order fires several different orders in one call (a long/short pair).
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# Each basket leg is its own dictionary, and basket legs use the key "pricetype"
# (no underscore) -- unlike placeorder and splitorder, which use price_type=.
orders = [
    {"symbol": "RELIANCE", "exchange": "NSE", "action": "BUY",
     "quantity": 1, "pricetype": "MARKET", "product": "CNC"},
    {"symbol": "INFY", "exchange": "NSE", "action": "SELL",
     "quantity": 1, "pricetype": "MARKET", "product": "CNC"},
]

response = client.basketorder(orders=orders)

print(f"Basket status: {response['status']}")
for leg in response["results"]:
    print(f"  {leg['symbol']:10s} -> {leg['status']}  id {leg['orderid']}")
```

Live output

```
Basket status: success
  RELIANCE   -> success  id 26062381789276
  INFY       -> success  id 26062384311086
```

## Split orders: one big order, many small fills
A **split order** takes one large quantity and chops it into smaller child orders automatically. Two reasons to do this: very large F&O orders can exceed the exchange's **freeze quantity** (the maximum size allowed in one order), and breaking a big order into pieces reduces your **market impact** - the tendency of a single huge order to move the price against you. Give it a total `quantity` and a `splitsize`, and it does the arithmetic.
EX 7Split a large order into chunksMCXch25/07_split_order.py
Copy
```
# A split order chops one big order into smaller child orders automatically.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# Buy 5 lots of GOLDM but in chunks of 2 -> orders of 2, 2, 1. Useful for large
# F&O orders that exceed the exchange freeze limit, or to reduce market impact.
response = client.splitorder(
    symbol="GOLDM03JUL26FUT",
    exchange="MCX",
    action="BUY",
    quantity=5,
    splitsize=2,
    price_type="MARKET",
    product="NRML",
)

print(f"Status: {response['status']}  total {response['total_quantity']} in chunks of {response['split_size']}")
for leg in response["results"]:
    print(f"  order {leg['order_num']}: qty {leg['quantity']}  id {leg['orderid']}")
```

Live output

```
Status: success  total 5 in chunks of 2
  order 1: qty 2  id 26062343652068
  order 2: qty 2  id 26062346057578
  order 3: qty 1  id 26062348347937
```

## Modifying and cancelling
A resting limit or stop order isn't set in stone. As long as it hasn't filled, you can **modify** its price or quantity, or **cancel** it entirely. Modifying needs the order id plus the full order details (with the changed value); cancelling needs only the id. Here's the whole life of one order - placed, repriced, then pulled.
EX 8Modify then cancel a resting orderNSEch25/08_modify_cancel.py
Copy
```
# The full life of a resting order: place it, modify the price, then cancel it.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# 1) Place a LIMIT order that rests away from the market.
placed = client.placeorder(
    strategy="Chapter25", symbol="SBIN", exchange="NSE", action="BUY",
    price_type="LIMIT", product="CNC", quantity=1, price=700,
)
order_id = placed["orderid"]
print(f"Placed  : {order_id} at 700")

# 2) Modify it: raise the limit price to 710. Re-send the order's details.
modified = client.modifyorder(
    order_id=order_id, strategy="Chapter25", symbol="SBIN", exchange="NSE",
    action="BUY", price_type="LIMIT", product="CNC", quantity=1, price=710,
)
print(f"Modified: {modified['status']} -> new price 710")

# 3) Changed your mind? Cancel it by id.
cancelled = client.cancelorder(order_id=order_id, strategy="Chapter25")
print(f"Cancelled: {cancelled['status']}")
```

Live output

```
Placed  : 26062309011793 at 700
Modified: success -> new price 710
Cancelled: success
```

Heads up
You can only modify or cancel an order that is still **open/pending**. Once an order is complete, cancelled or rejected, it's frozen - there's nothing left to change. You also cannot flip an order's `action` (BUY to SELL) by modifying; cancel it and place a fresh one instead.
## Reading back what happened
Placing orders is only half the job; a real bot also _reads the market's reply_. Three books tell you everything:
  * **Order book** (`orderbook()`) - every order you sent today and its current state (complete, open, rejected...). Its `data` is a dictionary holding an `orders` list plus a `statistics` summary.
  * **Trade book** (`tradebook()`) - only the orders that actually _filled_ , with their fill prices. Its `data` is a plain list.
  * **Position book** (`positionbook()`) - what you currently _hold_ , with live P&L. Also a plain list.

EX 9Read the order bookNSEch25/09_orderbook.py
Copy
```
# Read the order book: every order you sent today and a summary of their states.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

book = client.orderbook()
data = book["data"]
orders = data["orders"]
stats = data["statistics"]

print(f"Orders today: {len(orders)}")
print(f"  completed: {stats['total_completed_orders']:.0f}  "
      f"open: {stats['total_open_orders']:.0f}  "
      f"rejected: {stats['total_rejected_orders']:.0f}")

# Show the five most recent orders.
for o in orders[:5]:
    print(f"  {o['action']:4s} {o['symbol']:16s} {o['pricetype']:7s} "
          f"qty {o['quantity']} -> {o['order_status']}")
```

Live output

```
Orders today: 192
  completed: 171  open: 3  rejected: 1
  BUY  SBIN             LIMIT   qty 1 -> cancelled
  BUY  GOLDM03JUL26FUT  MARKET  qty 1 -> complete
  BUY  GOLDM03JUL26FUT  MARKET  qty 2 -> complete
  BUY  GOLDM03JUL26FUT  MARKET  qty 2 -> complete
  SELL INFY             MARKET  qty 1 -> complete
```

EX 10Read trade and position booksNSEch25/10_trade_position_books.py
Copy
```
# Trade book = what actually FILLED. Position book = what you currently HOLD.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# Both books return their data as a list of dictionaries.
trades = client.tradebook()["data"]
print(f"Trades filled today: {len(trades)}")
for t in trades[:3]:
    print(f"  {t['action']:4s} {t['symbol']:16s} @ {t['average_price']}")

positions = client.positionbook()["data"]
open_pos = [p for p in positions if int(float(p["quantity"])) != 0]
print(f"\nOpen positions: {len(open_pos)}")
for p in open_pos[:5]:
    print(f"  {p['symbol']:16s} qty {p['quantity']:>4}  ltp {p['ltp']}  pnl {p['pnl']}")
```

Live output

```
Trades filled today: 171
  BUY  GOLDM03JUL26FUT  @ 144360.0
  BUY  GOLDM03JUL26FUT  @ 144360.0
  BUY  GOLDM03JUL26FUT  @ 144360.0

Open positions: 9
  RELIANCE         qty    6  ltp 1309.5  pnl 0.0
  INFY             qty   -1  ltp 1029.3  pnl 0.0
  SBIN             qty    1  ltp 1024.2  pnl 0.0
  GOLDM03JUL26FUT  qty    1  ltp 144336.0  pnl -293.01
  GOLDM03JUL26FUT  qty    5  ltp 144336.0  pnl -1076.0
```

Key idea
Notice the shapes differ: `orderbook()` returns `data` as a _dictionary_ (`orders` + `statistics`), while `tradebook()` and `positionbook()` return `data` as a plain _list_. When in doubt, print the response once and look before you reach into it - a habit that saves a lot of `KeyError` surprises.
## The panic buttons
Finally, two calls every trader should know cold. `cancelallorder()` wipes out every pending order in one shot. `closeposition()` squares off _every_ open position with market orders - a SELL for each long, a BUY for each short. Together they're your emergency exit and your end-of-day flatten.
EX 11Cancel all orders and close all positionsNSEch25/11_close_and_cancel_all.py
Copy
```
# The two "panic buttons": cancel every pending order and flatten every position.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

# cancelallorder() removes every open/pending order in one shot.
cancelled = client.cancelallorder(strategy="Chapter25")
print(f"Cancel all : {cancelled['status']} - {cancelled.get('message')}")

# closeposition() squares off every open position with market orders
# (a SELL for longs, a BUY for shorts). Your end-of-day flatten button.
closed = client.closeposition(strategy="Chapter25")
print(f"Close all  : {closed['status']} - {closed.get('message')}")

print("Use these for an emergency exit or a clean end-of-day square-off.")
```

Live output

```
Cancel all : success - Canceled 3 orders. Failed to cancel 0 orders.
Close all  : success - Closed 9 positions
Use these for an emergency exit or a clean end-of-day square-off.
```

Heads up
`closeposition()` is deliberately blunt: no confirmation, no selectivity - it flattens _everything_. That's exactly what you want in an emergency or at the closing bell, but never wire it to a hair-trigger. For closing one specific position, place a single counter order instead.
## Try it yourself
  * Run example 1, then place a market order and immediately read the order book - find your order in the list.
  * Change the smart-order `position_size` to 0 and predict what it should do before you run it.
  * Build a basket that buys two stocks you follow and shorts a third, then read the position book to confirm all three legs.


## Recap
  * **Always confirm analyze mode** before sending orders - it's a one-line pre-flight check.
  * An order is five answers: symbol+exchange, action, price_type, product, quantity. `placeorder`, `placesmartorder` and `splitorder` use `price_type=`; only `basketorder` legs use the key `pricetype` (no underscore).
  * **MARKET** fills now, **LIMIT** fills at your price or better, **SL/SL-M** are stops that wake on a trigger to protect you.
  * **Smart orders** trade to an absolute target size; **basket** fires many orders at once; **split** chops one big order into safe chunks.
  * You can **modify or cancel** only orders that are still open; read results from the **order, trade and position books**.
  * `cancelallorder()` and `closeposition()` are your panic buttons - powerful, blunt, and best used deliberately.


You can now place and manage any order through code. Next we change gears completely: before risking a rupee on these orders, we'll prove a strategy actually has an edge - by building a backtest from scratch and then with VectorBT.
On this page
