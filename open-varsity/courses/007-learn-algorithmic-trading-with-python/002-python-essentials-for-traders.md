Chapters
Module A · Foundations - Chapter 02
# Python Essentials for Traders
The Python you actually need - variables, lists, dicts, loops and functions, in a trading context.
NSE
What you'll learn
  * ·Numbers & P&L math
  * ·Lists & dicts of positions
  * ·Loops over symbols
  * ·Functions for reusable logic
  * ·Conditionals for signals
  * ·Handling SDK responses


Here's a promise: you do not need a computer science degree to automate your trading. You need a _working_ grasp of about six ideas - numbers, text, lists, dictionaries, loops, and functions. That's genuinely it. Master those six and you can read and write the code in every remaining chapter of this series.
So if you've never written a line of Python, this is your chapter. We'll go slowly, define every word, and ground every idea in something you already understand: trades, prices, watchlists, and profit. If you _do_ know Python, skim the headings and meet me in Chapter 3.
Note
Run each example as you read. Type it, change a number, run it again. Programming is a contact sport - you learn it in your fingers, not just your eyes. Use `uv run python the_file.py` to run any example, as we set up in Chapter 1.
## Libraries, modules, and imports
You will almost never write everything from scratch. Most of your power as a trader-programmer comes from **libraries** other people have already built and tested. Three words to get straight, because they sit at the top of every script you'll write:
  * A **library** (also called a _package_) is a collection of ready-made code you install once and reuse forever. `openalgo` is a library. So are `pandas`, `numpy`, `matplotlib` and `seaborn`. You install one with `uv add <name>` (we did `uv add openalgo` in Chapter 1).
  * A **module** is a labelled compartment _inside_ a library that groups related tools. Inside `openalgo`, the order and data tools live in one place and the 80-plus indicators live in a module called `ta`. You reach into a module with a dot: `openalgo.ta`.
  * A **function** is a named action that does one job - you "call" it by writing its name with parentheses, often handing it some inputs. `round(2275.0)` calls the built-in `round` function. `client.history(...)` calls the `history` function to fetch candles.


**import** is how you pull a library or module into your script so you can use its functions. Two forms appear everywhere:

```
import openalgo              # bring in the whole library; use it as openalgo.something
from openalgo import api     # bring just the `api` tool straight into your script
from openalgo import api, ta # bring in two things at once

```

That second form is exactly why our scripts open with `from openalgo import api` and then build `client = api(...)`: we _imported_ the `api` tool from the `openalgo` library, then _used_ it.
Key idea
The dot `.` simply means "inside" or "belonging to". Read `openalgo.ta.rsi(...)` right to left: the `rsi` function, inside the `ta` module, inside the `openalgo` library. And `client.history(...)` means the `history` action belonging to your `client`. A function attached to an object like this is also called a **method** - same idea as a function, just bundled with the thing it acts on. Once the dot clicks, the whole SDK stops looking mysterious: it's just tools nested inside tools.
## Numbers: the language of profit and loss
Everything in trading eventually becomes a number. A **variable** is just a labelled box that holds a value - you put something in it, give it a name, and use that name later. Writing `entry_price = 1300.0` creates a box called `entry_price` holding the number `1300.0`.
Trading is then mostly arithmetic. Profit on a trade is `(exit price - entry price) x quantity`. Your return, as a percentage, is that profit divided by what you paid, times 100. Python does this with the ordinary symbols `+ - * /`, and `round()` trims a long decimal to something readable.
EX 1Profit and return of a tradech02/01_numbers_pnl.py
Copy
```
# Python numbers do your trade math. Compute the P&L of a single trade.
entry_price = 1300.0
exit_price = 1345.5
quantity = 50

pnl = (exit_price - entry_price) * quantity
pnl_pct = (exit_price - entry_price) / entry_price * 100

print("Profit/Loss:", round(pnl, 2))
print("Return %   :", round(pnl_pct, 2))
```

Live output

```
Profit/Loss: 2275.0
Return %   : 3.5
```

Read that output as a real trade: you bought 50 shares at 1300, sold at 1345.50, and walked away with ₹2,275 - a 3.5% return. The computer just did what you'd do on a notepad, instantly and without arithmetic slips.
## Strings: naming what you trade
A **string** is text - letters and symbols wrapped in quotes, like `"RELIANCE"` or `"BUY"`. Every symbol, exchange, and order action you'll ever use is a string.
The most useful tool for strings is the **f-string**. Put the letter `f` immediately before the opening quote, and you can drop variables straight into the text inside curly braces `{ }`. You can even format them: `{price:.2f}` shows two decimal places, and `{value:,.2f}` adds commas for thousands. This is how you turn raw numbers into a tidy, human-readable line.
EX 2Format an order summarych02/02_strings.py
Copy
```
# Build a clean, human-readable order summary with an f-string.
symbol = "RELIANCE"
action = "BUY"
qty = 50
price = 1309.5

summary = f"{action} {qty} x {symbol} @ {price:.2f}  =  Rs.{qty * price:,.2f}"
print(summary)

# A few handy string methods you will use on symbols and exchanges:
print(symbol.lower(), "|", action.title(), "|", "nfo".upper())
```

Live output

```
BUY 50 x RELIANCE @ 1309.50  =  Rs.65,475.00
reliance | Buy | NFO
```

Tip
`{price:.2f}` means "two decimal places" -> `1309.50`. `{value:,.2f}` adds thousands separators -> `65,475.00`. You'll format prices and P&L constantly, so these two tricks pay for themselves within a day.
## Lists: your watchlist
A **list** is an ordered collection of things, written inside square brackets: `["RELIANCE", "TCS", "INFY"]`. If a variable is one box, a list is a row of boxes in a fixed order. It's the natural way to hold a watchlist.
A few things you can do with any list:
  * Read one item by its **position** (Python counts from `0`, so `watchlist[0]` is the first).
  * Take a **slice** - a sub-range - with `watchlist[:2]` (the first two).
  * **Grow** it with `.append("HDFCBANK")`.
  * **Loop** over every item (more on loops shortly).

EX 3Work with a watchlistch02/03_lists_watchlist.py
Copy
```
# A watchlist is just a list. Index it, slice it, grow it, loop over it.
watchlist = ["RELIANCE", "TCS", "INFY", "SBIN"]

print("First symbol :", watchlist[0])
print("Last symbol  :", watchlist[-1])
print("First two    :", watchlist[:2])

watchlist.append("HDFCBANK")  # add a symbol
print("How many     :", len(watchlist))

for i, sym in enumerate(watchlist, start=1):
    print(i, sym)
```

Live output

```
First symbol : RELIANCE
Last symbol  : SBIN
First two    : ['RELIANCE', 'TCS']
How many     : 5
1 RELIANCE
2 TCS
3 INFY
4 SBIN
5 HDFCBANK
```

Heads up
Counting from zero trips up every beginner. The _first_ item is `[0]`, the _second_ is `[1]`, and so on. The handy shortcut `[-1]` means "the last item". Say it out loud a few times - it'll stick.
## Dictionaries: how OpenAlgo talks to you
This one matters more than any other in this chapter, so let's be deliberate. A **dictionary** (or "dict") stores information as **key: value** pairs inside curly braces - like a labelled form. Instead of remembering that position number 3 is the price, you just ask for `position["avg_price"]`. Each key is a label; each value is what's stored under it.
Why does this matter so much? Because **every response from the OpenAlgo SDK is a dictionary.** When you wrote `q["ltp"]` and `funds["data"]` in Chapter 1, you were reading dictionaries. Learn to build and read them, and you can read every answer the market gives you.
EX 4Model a position as a dictionarych02/04_dicts_position.py
Copy
```
# OpenAlgo returns data as dictionaries, so model a position as one too.
position = {"symbol": "SBIN", "exchange": "NSE", "qty": 750, "avg_price": 812.4}

print("Symbol      :", position["symbol"])
print("Invested    :", position["qty"] * position["avg_price"])

position["ltp"] = 818.0  # add a new key
position["pnl"] = (position["ltp"] - position["avg_price"]) * position["qty"]

print("Live P&L    :", round(position["pnl"], 2))
print("All fields  :", list(position.keys()))
```

Live output

```
Symbol      : SBIN
Invested    : 609300.0
Live P&L    : 4200.0
All fields  : ['symbol', 'exchange', 'qty', 'avg_price', 'ltp', 'pnl']
```

Key idea
A quote response looks like `{"status": "success", "data": {"ltp": 1309.5, ...}}`. Notice it's a dictionary _inside_ a dictionary. To reach the price you go `response["data"]["ltp"]` - first open the `"data"` box, then read `"ltp"` from inside it. That nested lookup is the single most common pattern in the entire SDK, so get comfortable with it now.
## Loops: do it for every symbol
A **loop** repeats an action automatically. A `for` loop says "for each item in this list, do the following." Pair a loop with a list of symbols and you've built the engine behind every scanner in this series - instead of checking one stock, you check a hundred with the same few lines.
Here we loop over a watchlist and fetch each stock's live price. Read it as: _"for each symbol in my list, go ask OpenAlgo for its price and print it."_
EX 5Loop and fetch live pricesNSEch02/05_loop_quotes.py
Copy
```
# Loop over a watchlist and pull each live price from OpenAlgo.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

for sym in ["RELIANCE", "TCS", "INFY"]:
    ltp = client.quotes(symbol=sym, exchange="NSE")["data"]["ltp"]
    print(f"{sym:10s} {ltp:>10.2f}")
```

Live output

```
RELIANCE      1309.50
TCS           2059.60
INFY          1029.30
```

## Conditionals: making a decision
Trading is decisions, and **conditionals** are how code decides. The keywords `if`, `elif` (short for "else if"), and `else` let your program choose a path based on the data in front of it. _If the price is above its average, consider buying; else, stay out._ That sentence is already almost Python.
Here we classify a stock as up, down, or flat based on its change from yesterday's close - the seed of every trading rule you'll ever write.
EX 6Decide with if / elif / elseNSEch02/06_conditionals.py
Copy
```
# if / elif / else turn market data into a decision.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

q = client.quotes(symbol="RELIANCE", exchange="NSE")["data"]
change = q["ltp"] - q["prev_close"]

if change > 0:
    print(f"RELIANCE is UP {change:.2f} today")
elif change < 0:
    print(f"RELIANCE is DOWN {abs(change):.2f} today")
else:
    print("RELIANCE is flat")
```

Live output

```
RELIANCE is DOWN 17.00 today
```

## Functions: write once, reuse forever
A **function** is a reusable mini-program with a name. You define it once with the keyword `def`, hand it some inputs (called **parameters**), and it hands back a result with `return`. After that, you call it by name as many times as you like.
Why bother? Because you'll fetch a price hundreds of times. Write a `last_price()` function once, and from then on getting a price - for a stock on NSE or a commodity on MCX - is a single, readable call. Functions are how you stop repeating yourself.
EX 7A reusable last_price()NSEMCXch02/07_functions.py
Copy
```
# Wrap repeated work in a function you can reuse anywhere.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)


def last_price(symbol, exchange="NSE"):
    """Return the last traded price for any symbol on any exchange."""
    return client.quotes(symbol=symbol, exchange=exchange)["data"]["ltp"]


print("RELIANCE (NSE):", last_price("RELIANCE"))
print("GOLDM    (MCX):", last_price("GOLDM03JUL26FUT", "MCX"))
```

Live output

```
RELIANCE (NSE): 1309.5
GOLDM    (MCX): 144349
```

Functions can also take **default values** (so you can leave an input out and get a sensible fallback) and `return` a computed number. This `trade_pnl()` works for both a long trade (BUY) and a short trade (SELL), and defaults to a long if you don't say otherwise.
EX 8A P&L function for long and shortch02/08_function_pnl.py
Copy
```
# A function can take inputs (with defaults) and return a computed result.
def trade_pnl(entry, exit_price, qty, side="BUY"):
    """P&L for a long (BUY) or short (SELL) trade."""
    move = exit_price - entry if side == "BUY" else entry - exit_price
    return round(move * qty, 2)


print("Long  :", trade_pnl(1300, 1345, 50))           # bought low, sold higher
print("Short :", trade_pnl(1300, 1280, 50, "SELL"))   # sold high, bought back lower
print("Loser :", trade_pnl(1300, 1290, 50))
```

Live output

```
Long  : 2250
Short : 1000
Loser : -500
```

## Handling responses safely
Live code meets live problems: a mistyped symbol, a dropped connection, a market that's closed. Beginners write code that crashes at the first hiccup; professionals write code that _expects_ trouble. Two tools make that easy:
  * **Check the status** - most SDK responses include a `"status"` you can test before trusting the data.
  * **`try`/`except`** - put risky code in a `try` block, and if it fails, the `except` block runs instead of the whole program crashing.


Notice how the unknown symbol below returns a clean, readable message instead of a frightening error.
EX 9Guard against bad callsNSEch02/09_safe_responses.py
Copy
```
# Real code must handle errors. Check status and guard with try / except.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)


def safe_ltp(symbol, exchange="NSE"):
    try:
        resp = client.quotes(symbol=symbol, exchange=exchange)
        if resp.get("status") == "success":
            return resp["data"]["ltp"]
        return f"error: {resp.get('message', 'unknown')}"
    except Exception as exc:  # network or parsing problem
        return f"exception: {exc}"


print("Valid symbol  :", safe_ltp("RELIANCE"))
print("Unknown symbol:", safe_ltp("NOTASYMBOL"))
```

Live output

```
Valid symbol  : 1309.5
Unknown symbol: error: HTTP 400: {"message":"Symbol 'NOTASYMBOL' not found for exchange 'NSE'. Please verify the symbol name and ensure master contracts are downloaded.","status":"error"}
```

Tip
A bot that runs all day _will_ hit a bad response eventually. Wrapping market calls in `try`/`except` is the difference between a bot that logs a warning and keeps trading, and one that silently dies at 10:42 a.m. and leaves a position open. We'll lean on this habit throughout the series.
## Comprehensions: transform data in one line
Once you're comfortable with lists and loops, Python offers a beautiful shortcut called a **list comprehension** - a way to build a new list from an existing one in a single readable line. Read `[b - a for a, b in zip(closes, closes[1:])]` as "the difference between each price and the one before it." Here we turn a column of closing prices into a list of day-over-day changes, then count the up days - a small preview of the data analysis we'll do at full scale with Pandas in Chapter 7.
EX 10Day-over-day changes in one lineNSEch02/10_comprehensions.py
Copy
```
# List comprehensions transform data in one readable line.
import os

from openalgo import api

client = api(
    api_key=os.getenv("OPENALGO_API_KEY", "your_api_key_here"),
    host=os.getenv("OPENALGO_HOST", "http://127.0.0.1:5000"),
)

df = client.history(symbol="SBIN", exchange="NSE", interval="D",
                    start_date="2026-06-01", end_date="2026-06-22")

closes = df["close"].tolist()
daily_change = [round(b - a, 2) for a, b in zip(closes, closes[1:])]
up_days = [c for c in daily_change if c > 0]

print("Last 5 closes :", closes[-5:])
print("Daily changes :", daily_change[-5:])
print("Up days       :", len(up_days), "of", len(daily_change))
```

Live output

```
Last 5 closes : [1015.3, 1026.5, 1042.7, 1035.1, 1040.75]
Daily changes : [-5.55, 11.2, 16.2, -7.6, 5.65]
Up days       : 11 of 15
```

## Try it yourself
  * In the P&L example, change the quantity to 100 and the exit price to a loss. Does the math match your head?
  * Add two stocks you actually follow to the watchlist loop and re-run it.
  * In the conditionals example, swap `RELIANCE` for an index future like `NIFTY30JUN26FUT` (with exchange `"NFO"`) and see it still works.


## Recap
  * A **variable** is a named box for a value; **numbers** compute P&L and returns, and `round()` tidies them.
  * **f-strings** like `f"{x:.2f}"` drop variables into text with clean formatting.
  * **Lists** hold watchlists - remember positions start at `0`, and `[-1]` is the last item.
  * **Dictionaries** are how the SDK returns _everything_ ; nested lookups like `r["data"]["ltp"]` are everywhere.
  * **Loops** repeat work across many symbols; **conditionals** (`if`/`elif`/`else`) turn data into decisions.
  * **Functions** package reusable logic; **try/except** keeps live code alive when something goes wrong.


That's the entire Python toolkit you need to follow this series. Everything from here builds on these six ideas. Next we get specific about the market itself: how OpenAlgo names every instrument across NSE, NFO and MCX - because getting the symbol right is half the battle.
On this page
