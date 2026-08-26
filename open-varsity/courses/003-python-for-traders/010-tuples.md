Chapters
Module 2 · Core Programming - Chapter 10
# Tuples
Fixed little groups of values - an OHLC bar, a row, a pair - that you don't want to change by accident.
PY
What you'll learn
  * ·Tuple vs list
  * ·Why immutability helps
  * ·Unpacking values
  * ·An OHLC bar as a tuple
  * ·Returning multiple values
  * ·When to use each


A list is wonderful precisely because it can change. But sometimes change is the _last_ thing you want. Think of a single day's price bar - its open, high, low and close. Those four numbers belong together as one fixed record; accidentally overwriting the "high" in the middle of your code would be a silent disaster. For locked-together groups like this, Python gives you the **tuple** : a list's quieter, sturdier cousin. It's a small chapter, but tuples unlock one genuinely lovely feature - unpacking - that you'll use constantly.
## A tuple: a group that can't change
You write a tuple with **round brackets** instead of square ones. You index it exactly like a list - but try to _change_ it, and Python firmly refuses:
EX 1An OHLC bar as a tuple - and why it won't let you edit itPYch10/01_tuple_basics.py
Copy
```
# A tuple groups values together with round brackets - and then locks them.
bar = (1300.0, 1318.4, 1297.2, 1313.6)   # open, high, low, close

print("The bar :", bar)
print("Open    :", bar[0])      # index it just like a list
print("Close   :", bar[-1])
print("Type    :", type(bar).__name__)

# Tuples are immutable - trying to change one raises an error (caught here safely).
try:
    bar[0] = 1305.0
except TypeError as e:
    print("Cannot change:", e)
```

Live output

```
The bar : (1300.0, 1318.4, 1297.2, 1313.6)
Open    : 1300.0
Close   : 1313.6
Type    : tuple
Cannot change: 'tuple' object does not support item assignment
```

That error isn't Python being difficult - it's Python protecting you. An OHLC bar is a fact about the past; it should never change once recorded. By making it a tuple, you make accidental edits _impossible_ rather than merely unlikely. That guarantee is the whole point.
Key idea
A **tuple** `(a, b, c)` is like a list but **immutable** - it can't be changed after you make it. Use round brackets `( )` instead of square `[ ]`. Index and slice it just like a list; you simply can't add, remove or overwrite items.
## Unpacking: many names in one line
Here's the feature that makes tuples a joy. **Unpacking** hands each value in a tuple its own variable name in a single, readable line:
EX 2Unpacking a bar, and the no-temp swap trickPYch10/02_unpacking.py
Copy
```
# Unpacking hands each value in a tuple its own name, in a single line.
bar = (1300.0, 1318.4, 1297.2, 1313.6)
open_, high, low, close = bar     # note: open_ avoids clashing with Python's open()

print("High :", high, " Low:", low)
print("Range:", round(high - low, 2))

# A neat side effect: swap two variables with no temporary holder.
support, resistance = 1300.0, 1325.0
support, resistance = resistance, support   # swapped in one line
print("After swap -> support:", support, "resistance:", resistance)
```

Live output

```
High : 1318.4  Low: 1297.2
Range: 21.2
After swap -> support: 1325.0 resistance: 1300.0
```

bar (a tuple, locked) 1300.0 1318.4 1297.2 1313.6 open_ high low close open_, high, low, close = bar - four values, four names, one clean line.
One line replaced four. Unpacking is everywhere in real Python - looping over rows, reading coordinates, taking results apart. It even gives you the elegant `a, b = b, a` swap, which trades two values without needing a temporary variable. (And notice we wrote `open_` with a trailing underscore: `open` is already the name of a built-in function, so we nudge ours aside to avoid a clash.)
## Returning several values
Tuples are also how Python functions hand back more than one answer. You've already used one such function without noticing - `divmod`:
EX 3divmod returns two values as a tuplePYch10/03_multiple_returns.py
Copy
```
# Some built-ins hand back several values at once - bundled as a tuple.
shares = 250
per_lot = 75
lots, leftover = divmod(shares, per_lot)   # divmod returns (quotient, remainder)
print("Full lots:", lots, " Leftover shares:", leftover)

# min() and max() work on a tuple exactly as they do on a list.
day = (1318.4, 1297.2, 1313.6)
print("Day high:", max(day), " Day low:", min(day))
```

Live output

```
Full lots: 3  Leftover shares: 25
Day high: 1318.4  Day low: 1297.2
```

`divmod(250, 75)` gives back `(3, 25)` - three full lots with 25 shares left over - as a single tuple, which we unpack into `lots` and `leftover` on the spot. When you write your own functions in Chapter 16, this is exactly how you'll return two or three results at once.
Did you know?
**The first photograph of a black hole was assembled in Python.** In 2019 the Event Horizon Telescope team turned petabytes of radio-telescope data into that now-famous orange ring - and the scientific pipeline that did it leaned heavily on Python libraries like NumPy and matplotlib. The same humble tuples, lists and arrays you're learning are trusted to process data from the edge of the observable universe.
## When to use a tuple vs a list
A simple rule of thumb keeps you right:
  * Reach for a **tuple** when you have a **fixed group of related values** that belong together as one record - an OHLC bar, a `(latitude, longitude)`, a function's multiple results.
  * Reach for a **list** when you have a **collection that will grow, shrink or be reordered** - a watchlist, a running series of prices, today's trades.


Tip
A quick mental test: _"Would changing one of these on its own be a bug?"_ If yes - like editing just the "high" of a recorded bar - use a tuple and let Python enforce it. If the collection is _meant_ to change, use a list.
## Try it yourself
  * Make a tuple `point = (1313.6, 50)` for a price and quantity, then unpack it into `price, qty` and compute the position value.
  * Try to append to a tuple (`bar.append(5)`). Read the error - it confirms a tuple has no such method, by design.
  * Swap two prices `a, b = 100, 200` using the one-line trick, then print them to confirm.


## Recap
  * A **tuple** `(a, b, c)` is an **immutable** list - same indexing and slicing, but it can't be changed.
  * Immutability is a **feature** : it protects fixed records like an OHLC bar from accidental edits.
  * **Unpacking** spreads a tuple into named variables in one line (`open_, high, low, close = bar`) and powers the no-temp **swap** `a, b = b, a`.
  * Functions return **multiple values as a tuple** (as `divmod` does) - you unpack them on arrival.
  * Use a **tuple** for fixed groups, a **list** for collections that change.


Lists and tuples both find things by _position_ - first, second, third. But often you want to look something up by _name_ : "what's the price of RELIANCE?" For that there's the single most useful structure in all of finance code - the **dictionary** - and it's next.
On this page
