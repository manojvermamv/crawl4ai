Chapters
Module 3 · Libraries, Files & Robust Code - Chapter 18
# The Standard Library Tour
A quick tour of the free toolbox that ships with Python - dates, maths, randomness and JSON, no install needed.
PY
What you'll learn
  * ·datetime basics
  * ·math & statistics
  * ·random for simulation
  * ·json in & out
  * ·the csv module
  * ·Batteries included


Now that you can `import`, the whole standard library opens up - hundreds of modules, free with Python. You don't need to know them all; you need to know _which drawers exist_ so you can reach for the right one. This chapter is a quick guided tour of the drawers a trader opens most: dates, randomness for simulation, and the JSON that market data speaks. We'll keep each one brief - the deepest ones get their own chapters soon.
## datetime: working with the calendar
Markets run on a calendar, and the **`datetime`**module handles dates, times and the arithmetic between them:
EX 1A taste of the datetime modulePYch18/01_datetime.py
Copy
```
from datetime import date, timedelta

# A fixed date keeps this example's output stable (use date.today() for "now").
today = date(2026, 6, 25)

print("Date      :", today)
print("Day name  :", today.strftime("%A"))      # the weekday, spelled out
print("In 7 days :", today + timedelta(days=7))  # date maths with timedelta
print("Year      :", today.year)
```

Live output

```
Date      : 2026-06-25
Day name  : Thursday
In 7 days : 2026-07-02
Year      : 2026
```

`strftime` formats a date into readable text (here `"%A"` gives the weekday name), and **`timedelta`**lets you do date _maths_ - "what's the date 7 trading-ish days from now?" We used a fixed date so the output stays stable; in real code `date.today()` gives you the live date. There's much more here - parsing, time zones, market sessions - and Chapter 23 gives it the full treatment.
## random: simulation and chance
The **`random`**module generates random numbers - invaluable for _simulating_ markets when you want to see how a strategy behaves across many possible futures:
EX 2A five-day random walk with the random modulePYch18/02_random_sim.py
Copy
```
import random

random.seed(42)        # seeding makes the "random" results reproducible

# Simulate 5 days of a price taking a random walk of +/- up to 1% a day.
price = 100.0
for day in range(1, 6):
    move = random.uniform(-1, 1)         # a random percentage move
    price = price * (1 + move / 100)
    print(f"Day {day}: move {move:+.2f}%  ->  price {price:.2f}")
```

Live output

```
Day 1: move +0.28%  ->  price 100.28
Day 2: move -0.95%  ->  price 99.33
Day 3: move -0.45%  ->  price 98.88
Day 4: move -0.55%  ->  price 98.33
Day 5: move +0.47%  ->  price 98.80
```

`random.uniform(-1, 1)` draws a random percentage move, and we compound it to walk a price forward. The crucial line is `random.seed(42)`: it makes the randomness **reproducible** , so this simulation prints the same path every time you run it - and so will yours.
Did you know?
**Python's "random" numbers aren't truly random - and that's a feature.** Under the hood, the `random` module uses an algorithm called the _Mersenne Twister_ , which produces a sequence so enormously long it won't repeat in any practical lifetime. But give it the same **seed** and it replays the exact same "random" path every single time. For traders that's gold: it means a simulation or backtest can be reproduced perfectly, by you or anyone checking your work.
## json: the language of market APIs
When a trading or data API sends you a quote, it almost always arrives as **JSON** text. The **`json`**module translates between that text and Python dictionaries:
EX 3Converting between JSON text and a Python dictPYch18/03_json.py
Copy
```
import json

quote = {"symbol": "RELIANCE", "ltp": 1313.60, "change": 13.60}

# dumps: a Python dictionary -> a JSON text string (how APIs send data).
text = json.dumps(quote)
print("As JSON text:", text)

# loads: JSON text -> back into a Python dictionary you can use.
back = json.loads(text)
print("Back to dict:", back["ltp"])
```

Live output

```
As JSON text: {"symbol": "RELIANCE", "ltp": 1313.6, "change": 13.6}
Back to dict: 1313.6
```

`json.dumps` turns a dictionary into JSON text (to send or save); `json.loads` turns JSON text back into a dictionary (to read what you received). Notice the result is exactly the dictionaries you mastered in Chapter 11 - which is why JSON will feel familiar. Chapter 22 goes deeper, including nested data and reading from files.
## And many more drawers
Those are three favourites, but the toolbox is deep. A few more worth knowing exist:
datetimedates, times & durations mathroots, pi, rounding randomsimulation & sampling jsondata in and out csvsimple table files statisticsmean, median, stdev A few of the standard library's most useful drawers - all free, all built in.
Tip
Don't try to memorise the standard library - nobody has it all in their head. The skill is knowing _roughly_ what exists, then looking up the details when you need them. "Python has a module for that" is true astonishingly often; a quick search or a glance at the official docs fills in the rest. (We'll practise exactly this look-it-up skill in Chapter 24.)
## Try it yourself
  * Use `datetime` to print the weekday name for `date(2026, 1, 1)`. What day does 2026 begin on?
  * Change the seed in the random walk to `random.seed(7)` and run it again - a different path, but reproducible. Remove the seed line entirely and run twice: now it differs each time.
  * Take the dictionary `{"a": 1, "b": [2, 3]}`, run it through `json.dumps`, and notice how the list survives the trip.


## Recap
  * The **standard library** gives you hundreds of ready modules; know which drawers exist and reach for them.
  * **`datetime`**handles dates, formatting (`strftime`) and date maths (`timedelta`).
  * **`random`**generates numbers for simulation;**`random.seed()`**makes results reproducible.
  * **`json`**converts between JSON text and Python dictionaries (`dumps` out, `loads` in).
  * Many more drawers exist - **`math`**,**`statistics`**,**`csv`**,**`os`**- so look things up rather than memorising.


Everything so far has come _free_ with Python. But the most powerful tools for a trader - NumPy, pandas, yfinance - aren't in the standard library; you have to install them. In the next chapter we'll do exactly that with **pip** , and learn to keep projects tidy with **virtual environments**.
On this page
