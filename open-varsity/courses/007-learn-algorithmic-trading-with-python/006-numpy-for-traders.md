Chapters
Module A · Foundations - Chapter 06
# NumPy for Traders
NumPy fundamentals for traders - creating arrays, indexing, vectorised math and the everyday functions, on simple price data.
NSEINDEX
What you'll learn
  * ·Creating arrays & helpers
  * ·Shape, size & dtype
  * ·Indexing & slicing
  * ·Vectorised math & broadcasting
  * ·Aggregations, masks & np.where
  * ·2D arrays & the axis argument


Before you can compute returns, indicators or a backtest, you need the tool that does fast number-crunching in Python: **NumPy** (say "num-pie"). It's the engine underneath pandas, the indicator library and the backtester you'll meet later, so a little NumPy now pays off everywhere.
This chapter keeps it simple. We'll learn the core ideas on small, hand-typed arrays of Indian stock prices - no data download, no SDK, just `import numpy as np` and the basics every trader actually uses. Work through it once and the rest of the course will feel familiar.
## Creating an array
An **array** is NumPy's version of a list - an ordered row of numbers - but built for maths. You make one from a Python list, and NumPy also gives you ready-made arrays for common needs.
EX 1Make arrays a few different waysNSEch06/01_creating_arrays.py
Copy
```
# NumPy basics for traders -- everything starts with creating an array.
import numpy as np

# An array from a Python list: five daily closes of RELIANCE (in rupees).
closes = np.array([1305.0, 1298.5, 1310.4, 1318.6, 1312.7])
print("From a list :", closes)

# Handy ready-made arrays:
print("arange      :", np.arange(1, 6))           # 1..5, like range()
print("zeros       :", np.zeros(5))               # five 0.0s (empty P&L slots)
print("ones        :", np.ones(3))                # three 1.0s
print("full        :", np.full(4, 100))           # four 100s (e.g. lot sizes)
print("linspace    :", np.linspace(100, 200, 5))  # 5 evenly spaced, 100 to 200
```

Live output

```
From a list : [1305.  1298.5 1310.4 1318.6 1312.7]
arange      : [1 2 3 4 5]
zeros       : [0. 0. 0. 0. 0.]
ones        : [1. 1. 1.]
full        : [100 100 100 100]
linspace    : [100. 125. 150. 175. 200.]
```

`np.array([...])` wraps your own numbers; `arange`, `zeros`, `ones`, `full` and `linspace` build common patterns without typing every value.
## Shape, size and dtype
Every array carries a few facts about itself. You'll check these constantly when something doesn't line up.
EX 2What an array knows about itselfNSEch06/02_array_attributes.py
Copy
```
# Every array knows its own shape, size and data type.
import numpy as np

closes = np.array([1305.0, 1298.5, 1310.4, 1318.6, 1312.7])

print("Array    :", closes)
print("shape    :", closes.shape)    # (5,) -> 5 elements in one row
print("ndim     :", closes.ndim)     # 1  -> one dimension
print("size     :", closes.size)     # 5  -> total count
print("dtype    :", closes.dtype)    # float64 -> decimal numbers

qty = np.array([10, 25, 15])
print("int dtype:", qty.dtype)       # int64 -> whole numbers (e.g. quantities)
```

Live output

```
Array    : [1305.  1298.5 1310.4 1318.6 1312.7]
shape    : (5,)
ndim     : 1
size     : 5
dtype    : float64
int dtype: int64
```

`shape` is its dimensions, `ndim` the number of them, `size` the total count, and `dtype` the kind of number inside - `float64` for prices, `int64` for whole quantities.
## Indexing and slicing
You reach into an array by position, exactly like the lists from Chapter 2. The one you'll use most is `[-1]` - "the latest value".
EX 3Pick values by positionINDEXch06/03_indexing_slicing.py
Copy
```
# Reach into an array by position -- the same indexing you used for lists.
import numpy as np

# Ten days of NIFTY closing values.
nifty = np.array([25900, 25960, 25840, 25990, 26050,
                  26010, 25880, 25930, 26100, 26075])

print("First day   :", nifty[0])
print("Latest day  :", nifty[-1])     # -1 is "most recent" -- used constantly
print("Days 2 to 4 :", nifty[1:4])    # positions 1,2,3 (the stop is excluded)
print("Last 5 days :", nifty[-5:])
print("Every 2nd   :", nifty[::2])    # a step of 2
```

Live output

```
First day   : 25900
Latest day  : 26075
Days 2 to 4 : [25960 25840 25990]
Last 5 days : [26010 25880 25930 26100 26075]
Every 2nd   : [25900 25840 26050 25880 26100]
```

A slice `a[1:4]` takes positions 1, 2 and 3 (the end is excluded), `a[-5:]` takes the last five, and `a[::2]` steps in twos.
## Vectorised math and broadcasting
Here's the superpower. Do maths on a whole array in one stroke - no loop. Combine an array with a single number and NumPy "broadcasts" that number across every element; combine two equal-length arrays and it works element by element.
EX 4Math on the whole array at onceNSEch06/04_vectorised_math.py
Copy
```
# Vectorisation: do the math on the WHOLE array at once -- no loops.
import numpy as np

closes = np.array([1305.0, 1298.5, 1310.4, 1318.6, 1312.7])

# Broadcasting: combine an array with a single number.
print("After 5% rise :", np.round(closes * 1.05, 2))
print("Minus 10 rs   :", closes - 10)

# Two arrays, multiplied element by element: price x quantity held.
qty = np.array([10, 10, 20, 20, 15])
value = closes * qty
print("Holding value :", value)
print("Total value   :", value.sum())
```

Live output

```
After 5% rise : [1370.25 1363.42 1375.92 1384.53 1378.34]
Minus 10 rs   : [1295.  1288.5 1300.4 1308.6 1302.7]
Holding value : [13050.  12985.  26208.  26372.  19690.5]
Total value   : 98305.5
```

Tip
Whenever you're about to write a `for` loop over prices, pause - there's almost always a vectorised one-liner. On a year of data it can be hundreds of times faster, and it reads like the maths it represents.
## The summary functions
These are the everyday questions you ask of any price series - the average, the extremes, the spread - each a single call.
EX 5Mean, min, max, std and moreNSEch06/05_aggregations.py
Copy
```
# The summary functions a trader reaches for every day.
import numpy as np

closes = np.array([1305.0, 1298.5, 1310.4, 1318.6, 1312.7])

print("mean   :", round(closes.mean(), 2))    # average close
print("max    :", closes.max())               # highest
print("min    :", closes.min())               # lowest
print("std    :", round(closes.std(), 2))     # spread -- a volatility proxy
print("median :", np.median(closes))
print("sum    :", closes.sum())
print("cumsum :", np.cumsum(closes))          # running total
```

Live output

```
mean   : 1309.04
max    : 1318.6
min    : 1298.5
std    : 6.84
median : 1310.4
sum    : 6545.2
cumsum : [1305.  2603.5 3913.9 5232.5 6545.2]
```

`std` (standard deviation) measures how spread-out the numbers are - your first taste of volatility - and `cumsum` gives a running total.
## Boolean masks and np.where
Compare an array to something and you don't get one True/False - you get a **mask** , a True/False for _every_ element. Use it to filter (keep only the `True` ones) or count, and use `np.where` to label each element in one go.
EX 6Ask a question of every elementNSEch06/06_boolean_masks.py
Copy
```
# Ask a yes/no question of every element, then filter or count.
import numpy as np

closes = np.array([1305.0, 1298.5, 1310.4, 1318.6, 1312.7])
avg = closes.mean()

mask = closes > avg                        # True/False for each day
print("Above average?:", mask)
print("Those closes  :", closes[mask])     # keep only the True ones
print("How many days :", mask.sum())       # True counts as 1

# np.where labels every element in one stroke (1 = above avg, 0 = not).
tags = np.where(closes > avg, 1, 0)
print("Tags          :", tags)
```

Live output

```
Above average?: [False False  True  True  True]
Those closes  : [1310.4 1318.6 1312.7]
How many days : 3
Tags          : [0 0 1 1 1]
```

This filter-by-condition pattern is the literal seed of every trading **signal** you'll build later - an entry is just a mask that's `True` when your rule is met.
## Popular functions to know
A short grab-bag you'll reach for again and again on price data.
EX 7Functions worth memorisingNSEch06/07_handy_functions.py
Copy
```
# A grab-bag of popular NumPy functions you'll use on price data.
import numpy as np

closes = np.array([1305.0, 1298.5, 1310.4, 1318.6, 1312.7])

print("diff    :", np.diff(closes))               # day-to-day change
print("abs     :", np.abs(np.diff(closes)))       # size of move, sign dropped
print("round   :", np.round(closes, 0))           # round to whole rupees
print("sqrt    :", np.round(np.sqrt(closes), 1))
print("maximum :", np.maximum(closes, 1310))      # floor each value at 1310
print("sort    :", np.sort(closes))               # ascending
print("unique  :", np.unique([5, 5, 10, 20, 20])) # distinct values, sorted
```

Live output

```
diff    : [-6.5 11.9  8.2 -5.9]
abs     : [ 6.5 11.9  8.2  5.9]
round   : [1305. 1298. 1310. 1319. 1313.]
sqrt    : [36.1 36.  36.2 36.3 36.2]
maximum : [1310.  1310.  1310.4 1318.6 1312.7]
sort    : [1298.5 1305.  1310.4 1312.7 1318.6]
unique  : [ 5 10 20]
```

`diff` gives day-to-day changes, `abs` drops the sign, `round` tidies decimals, `maximum` floors values, and `sort`/`unique` reorder and de-duplicate.
## A quick look at 2D arrays
Real market data is often a table - several stocks over several days. That's a **2D array** : rows and columns. The key new idea is `axis`: `axis=1` works across each row, `axis=0` down each column.
EX 8Rows, columns and the axis argumentNSEch06/08_2d_arrays.py
Copy
```
# A 2D array is a table: here three stocks (rows) over four days (columns).
import numpy as np

# rows = RELIANCE, TCS, INFY ; columns = Mon..Thu closes
prices = np.array([
    [1305.0, 1298.5, 1310.4, 1312.7],
    [2068.0, 2090.5, 2075.0, 2081.25],
    [1052.0, 1041.3, 1055.8, 1048.5],
])

print("shape        :", prices.shape)        # (3, 4) -> 3 rows, 4 columns
print("INFY row     :", prices[2])           # the third stock
print("Thu column   :", prices[:, -1])       # last day, every stock
print("Per-stock avg:", np.round(prices.mean(axis=1), 1))  # across each row
print("Per-day avg  :", np.round(prices.mean(axis=0), 1))  # down each column
print("Reshaped     :", np.arange(6).reshape(2, 3))
```

Live output

```
shape        : (3, 4)
INFY row     : [1052.  1041.3 1055.8 1048.5]
Thu column   : [1312.7  2081.25 1048.5 ]
Per-stock avg: [1306.6 2078.7 1049.4]
Per-day avg  : [1475.  1476.8 1480.4 1480.8]
Reshaped     : [[0 1 2]
 [3 4 5]]
```

`prices[2]` picks a row (one stock), `prices[:, -1]` picks a column (one day across all stocks), and `reshape` rearranges the same numbers into a new shape.
## Try it yourself
  * Change the numbers in `closes` to a stock you follow and re-run the aggregations - is its `std` larger or smaller than RELIANCE's?
  * In the mask example, switch `> avg` to `< avg` to keep the below-average days instead.
  * In the 2D example, add a fourth stock as a new row and confirm the per-stock average still lines up.


## Recap
  * An **array** (`np.array`) is a row of numbers built for maths; `arange`, `zeros`, `ones`, `full`, `linspace` build common ones.
  * Check `shape`, `ndim`, `size` and `dtype` to understand any array.
  * **Index and slice** by position - `[-1]` is the latest, `a[-5:]` the last five, `a[::2]` every second.
  * **Vectorised math** and **broadcasting** apply an operation to the whole array at once - no loops.
  * Summaries (`mean`, `max`, `min`, `std`, `median`, `cumsum`) and handy functions (`diff`, `abs`, `round`, `maximum`, `sort`, `unique`) turn raw numbers into answers.
  * **Boolean masks** + `np.where` ask a question of every element - the seed of every signal.
  * **2D arrays** are tables; the `axis` argument chooses rows (`axis=1`) or columns (`axis=0`).


That's the fast-math foundation. Next we wrap these arrays in **pandas** - labelled tables with dates, rolling windows and group-bys - where real market analysis gets comfortable.
On this page
