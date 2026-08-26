Chapters
Module 2 · Core Programming - Chapter 16
# Functions
Wrap a calculation in a name and reuse it forever. Write 'percentage_change' once, call it a thousand times.
PY
What you'll learn
  * ·Defining a function
  * ·Arguments & return
  * ·A reusable P&L function
  * ·Default arguments
  * ·Docstrings
  * ·Why functions matter


Notice something about the last few chapters: you keep writing the _same_ little calculations - percentage change, profit, position value - over and over. Copying a formula around is how bugs breed: fix it in one place, forget the other four, and now your code disagrees with itself. The cure is the **function** : write a calculation _once_ , give it a name, and call it forever after. Functions are how every real program is built - small, named, trustworthy pieces snapped together. This chapter closes Module 2, and it's the most important idea in it.
## Defining a function
You create a function with **`def`**, a name, its inputs (**parameters**) in brackets, and a block that ends by handing back a result with **`return`**:
EX 1One function, called three timesPYch16/01_define.py
Copy
```
# A function packages a calculation under a name, so you can reuse it.
def percentage_change(old, new):
    return (new - old) / old * 100      # "return" hands the answer back

# Define it once, then call it as often as you like with different inputs.
print("RELIANCE:", round(percentage_change(1300, 1313.60), 2), "%")
print("TCS     :", round(percentage_change(2120, 2109.00), 2), "%")
print("INFY    :", round(percentage_change(1050, 1056.60), 2), "%")
```

Live output

```
RELIANCE: 1.05 %
TCS     : -0.52 %
INFY    : 0.63 %
```

old = 1300 new = 1313.60 percentage_change( old, new ) return 1.05 % A function is a machine: inputs go in, a result comes out. Build it once, use it anywhere.
Think of a function as a little machine. You feed it inputs (here `old` and `new`), it does its work, and `return` sends a value back out. We defined `percentage_change` once and called it three times with different stocks - no copy-paste, no chance of the formula drifting between uses.
Key idea
Define a function with **`def name(parameters):`**and end it with**`return value`**to send a result back.**Calling** it - `name(arguments)` - runs the block with those inputs and gives you the returned value.
## Default arguments and docstrings
Parameters can have **default values** , used when the caller doesn't supply one. And a string on the first line - a **docstring** - documents what the function does:
EX 2Defaults you can override, and a documenting docstringPYch16/02_defaults_docstring.py
Copy
```
def brokerage(turnover, rate=0.0003, cap=20.0):
    """Return the brokerage on a trade: a rate of turnover, capped at `cap` rupees."""
    return round(min(turnover * rate, cap), 2)    # round to paise

# rate and cap have DEFAULTS, so you can leave them out...
print("Small trade:", brokerage(10000))             # 0.0003 * 10000 = 3.0
print("Large trade:", brokerage(500000))            # would be 150, but capped at 20
# ...or override them by name.
print("Custom rate:", brokerage(10000, rate=0.001))  # 10.0

# A docstring documents the function and is readable via .__doc__
print("Docs       :", brokerage.__doc__)
```

Live output

```
Small trade: 3.0
Large trade: 20.0
Custom rate: 10.0
Docs       : Return the brokerage on a trade: a rate of turnover, capped at `cap` rupees.
```

Because `rate` and `cap` have defaults, `brokerage(10000)` just works; but you can override any of them by name, like `rate=0.001`. This is the flat-fee-capped model many discount platforms use - a small percentage, capped at a flat 20. The docstring, meanwhile, is free documentation: tools and editors read it, and so can you via `brokerage.__doc__`.
Tip
Get into the habit of writing a **one-line docstring** for every function: a short sentence saying what it returns. Future-you, reading this code in six months, will be grateful - and it costs you ten seconds now.
## Returning several values
A function can hand back more than one result by returning them comma-separated - which, as you learned in Chapter 10, bundles them into a tuple you can unpack on arrival:
EX 3A function returning profit and percentage togetherPYch16/03_multiple_return.py
Copy
```
def trade_summary(buy, sell, qty):
    """Return (profit, percent_change) for a completed round-trip trade."""
    profit = (sell - buy) * qty
    pct = (sell - buy) / buy * 100
    return profit, pct                  # two values come back as a tuple

# Unpack the two returned values straight into two names.
profit, pct = trade_summary(1300, 1313.60, 50)
print(f"Profit: {profit:,.2f}")
print(f"Move  : {pct:+.2f}%")
```

Live output

```
Profit: 680.00
Move  : +1.05%
```

`return profit, pct` sends back both numbers; `profit, pct = trade_summary(...)` catches them in two names. One call, two answers - tidy.
Did you know?
**NASA uses Python to explore space.** The Jet Propulsion Laboratory - the team behind the Mars rovers - leans on Python across its data analysis and mission-planning pipelines, sifting the images and telemetry that come back from other worlds. The functions their scientists write have the exact same `def name(...): return ...` shape you just learned. The humble function scales from a brokerage calculator to interplanetary science.
## Why functions matter
It's worth saying plainly why this idea is such a big deal:
  * **Write once, fix once.** A bug in `percentage_change` is fixed in _one_ place, and every caller is instantly correct.
  * **Names are documentation.** `brokerage(turnover)` tells a reader what's happening; a bare formula does not.
  * **Build big from small.** Every large program is just many small functions calling one another. Master the small piece and the large ones stop being scary.


This is the heartbeat of all software, and from here on you'll write functions constantly without thinking twice.
## Try it yourself
  * Write a function `position_value(price, qty)` that returns `price * qty`, and call it for 50 shares at 1313.60.
  * Give your function a default `qty=1`, so `position_value(1313.60)` returns the price of a single share.
  * Write a function that returns _both_ the brokerage and the turnover for a trade, and unpack the two results when you call it.


## Recap
  * A **function** packages reusable logic: **`def name(params):`**...**`return value`**.
  * **Default arguments** make parameters optional; override them by name when needed.
  * A **docstring** (first-line string) documents what a function does - write one every time.
  * Functions can **return several values** as a tuple, unpacked by the caller.
  * Functions mean **write-once, fix-once** code, readable names, and big programs built from small pieces.


That completes **Module 2** - you now have data structures, decisions, loops, comprehensions and functions. You can write real, self-contained programs. In **Module 3** we stop reinventing wheels and start _borrowing_ them: importing Python's vast libraries, installing new ones, reading and writing files, handling dates, and fixing errors with confidence. First up: **modules and imports**.
On this page
