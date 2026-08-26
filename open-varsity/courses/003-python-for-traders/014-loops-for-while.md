Chapters
Module 2 · Core Programming - Chapter 14
# Loops: for & while
Do something to every price in a series without writing it a hundred times - the heartbeat of all data work.
PYNSE
What you'll learn
  * ·The for loop
  * ·Looping over prices
  * ·range() & enumerate
  * ·while loops
  * ·break & continue
  * ·Accumulating a total


A watchlist has dozens of stocks. A year of prices has 250 days. A backtest might run over thousands of bars. You are _not_ going to write a line of code for each one - and you don't have to. The **loop** is the engine that says "do this for every item," and it's where the computer's real advantage over a human kicks in: tireless, instant repetition. This is one of the most important chapters in the course, so let's get it right.
## The for loop
The `for` loop walks through a collection - a list, a string, the keys of a dictionary - and runs its indented block once for **each** item. A favourite pattern is _accumulating_ a running total as you go:
EX 1Looping over prices to total and number themPYch14/01_for_loop.py
Copy
```
closes = [101.2, 103.5, 102.8, 104.1, 105.6]

# A for loop visits each item in the list, one at a time.
total = 0.0
for price in closes:
    total += price            # accumulate a running sum
print("Sum of closes:", round(total, 2))
print("Average      :", round(total / len(closes), 2))

# enumerate() hands you the position AND the value together.
for day, price in enumerate(closes, start=1):
    print(f"Day {day}: {price}")
```

Live output

```
Sum of closes: 517.2
Average      : 103.44
Day 1: 101.2
Day 2: 103.5
Day 3: 102.8
Day 4: 104.1
Day 5: 105.6
```

anotherprice? yes total += price repeat for the next item no print(total) A loop runs its body once per item, then moves on - until there are none left.
The variable `price` takes the value of each element in turn; `total += price` is shorthand for "add `price` to `total`." After five trips, `total` holds the sum. And **`enumerate()`**is a small gift: it hands you the position _and_ the value together, so you can number your output (`start=1` makes it count from 1 like a human, not 0).
Key idea
A **`for`loop** runs its indented block once for every item in a collection: `for price in closes:`. Use it to read, total, transform, or check each element. **`enumerate()`**adds a running position alongside each value.
## Counting with range(), and the while loop
Sometimes you want to loop a fixed number of times rather than over a collection. That's what **`range()`**is for - it produces a sequence of numbers. And when you don't know _how many_ times in advance - you just want to keep going _while_ something is true - you reach for a **`while`**loop:
EX 2range() to count, while to repeat until donePYch14/02_range_while.py
Copy
```
# range() generates a sequence of numbers - perfect for counting.
for i in range(1, 6):          # 1, 2, 3, 4, 5  (stops just before 6)
    print(f"Lot {i}")

# A while loop repeats for as long as its condition stays True.
capital = 100000
price = 1313.60
shares = 0
while capital >= price:        # keep buying while we can still afford one
    capital -= price
    shares += 1
print(f"Bought {shares} shares, {capital:,.2f} left over.")
```

Live output

```
Lot 1
Lot 2
Lot 3
Lot 4
Lot 5
Bought 76 shares, 166.40 left over.
```

`range(1, 6)` yields `1, 2, 3, 4, 5` - it stops _just before_ the end number, the same "up to but not including" rule as slicing. The `while` loop then keeps buying one share at a time _while_ we can still afford it, stopping the instant capital runs low: 76 shares, with 166.40 left.
Heads up
A `while` loop only ends when its condition becomes `False`, so **make sure something inside the loop moves it towards that**. If we forgot the `capital -= price` line, capital would never fall, the condition would stay `True` forever, and the program would hang in an **infinite loop**. (If that happens to you, press `Ctrl+C` to stop it.)
## break and continue
Two keywords give you finer control inside any loop. **`continue`**skips the rest of the current turn and jumps to the next item;**`break`**abandons the loop entirely:
EX 3Skipping with continue, stopping with breakPYch14/03_break_continue.py
Copy
```
prices = [101.2, 103.5, 99.8, 104.1, 98.5, 106.3]
alert_level = 105.0

# continue = skip the rest of THIS turn; break = stop the loop entirely.
for price in prices:
    if price < 100:
        continue                  # ignore sub-100 prices, jump to the next
    print("Checking", price)
    if price > alert_level:
        print("Alert! Price broke", alert_level)
        break                     # found it - no need to look further
```

Live output

```
Checking 101.2
Checking 103.5
Checking 104.1
Checking 106.3
Alert! Price broke 105.0
```

Watch the output: the sub-100 prices (`99.8`, `98.5`) never print, because `continue` skipped them. And the moment a price clears the alert level (`106.3`), `break` stops the scan - there's no point checking the rest. This "search until you find it, then stop" pattern is everywhere in real code.
Did you know?
**Reddit runs on Python.** One of the most-visited sites on the internet - billions of page views a month - has run on Python since 2005, when its founders rewrote it from another language to move faster. Every comment thread, vote and feed you've ever scrolled was served by loops, lists and dictionaries exactly like the ones in this chapter, just at enormous scale.
## Try it yourself
  * Loop over `closes` and print only the days where the price was above `103`. (Combine a `for` loop with an `if`.)
  * Use a `for i in range(...)` loop to print the 5-times table from `5` to `50`.
  * In the break/continue example, lower `alert_level` to `103`. Which price now triggers the alert, and which later prices go unchecked?


## Recap
  * A **`for`loop** repeats its block once per item in a collection - the core tool for processing prices, lists and more.
  * **`enumerate()`**gives position + value;**`range()`**generates a sequence of numbers to count with.
  * A **`while`loop** repeats _as long as_ a condition is True - be sure the condition can eventually turn False.
  * **`continue`**skips to the next item;**`break`**exits the loop early.


You've now noticed a recurring shape: take a list, loop over it, build a new list (of transformed or filtered values). Python has a beautiful one-line shorthand for exactly that, and once you see it you'll spot it everywhere. Next up: the **comprehension**.
On this page
