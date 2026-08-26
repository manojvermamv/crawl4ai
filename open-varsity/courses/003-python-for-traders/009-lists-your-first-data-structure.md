Chapters
Module 2 · Core Programming - Chapter 09
# Lists: Your First Data Structure
A watchlist, a week of closing prices, a basket of stocks - lists hold an ordered series you can grow, slice and sort.
PYNSE
What you'll learn
  * ·Making a list
  * ·Indexing & slicing
  * ·Adding & removing
  * ·Slicing a price series
  * ·Sorting & reversing
  * ·Useful list methods


Welcome to **Module 2**. So far each variable has held a _single_ value - one price, one symbol. But markets come in _series_ : a week of closing prices, a watchlist of stocks, the trades you did today. For that you need a container that holds many values at once, and the workhorse container in Python is the **list**. If you learn one data structure deeply, make it this one - lists are everywhere, and pandas (the heart of Module 4) is built right on top of the idea.
## Making a list
A list is values in order, written inside square brackets and separated by commas. Because it's ordered, you reach into it with exactly the same indexing and slicing you learned for strings:
EX 1A week of closes in a list, indexed and slicedPYch09/01_price_series.py
Copy
```
# A list holds many values in order, written inside square brackets.
closes = [101.2, 103.5, 102.8, 104.1, 105.6, 104.9, 106.3]   # a week of closes

print("All closes   :", closes)
print("How many     :", len(closes))
print("First (Mon)  :", closes[0])     # same indexing rules as strings
print("Last (today) :", closes[-1])
print("First three  :", closes[:3])    # a slice - Mon, Tue, Wed
print("Last two     :", closes[-2:])
```

Live output

```
All closes   : [101.2, 103.5, 102.8, 104.1, 105.6, 104.9, 106.3]
How many     : 7
First (Mon)  : 101.2
Last (today) : 106.3
First three  : [101.2, 103.5, 102.8]
Last two     : [104.9, 106.3]
```

Seven prices, one name. `closes[0]` is Monday's close, `closes[-1]` is today's, and `closes[:3]` slices out the first three days. Everything you learned about string positions - zero-based, negative-from-the-end, "stops just before" - works identically here. That's not a coincidence; Python keeps its rules consistent so what you learn once pays off everywhere.
## Growing and shrinking
Unlike a string, a list can be _changed_ - you add and remove items freely. This is what makes it perfect for a watchlist that grows and shrinks through the day:
EX 2Growing and shrinking a watchlistPYch09/02_add_remove.py
Copy
```
# Lists can grow and shrink - perfect for a changing watchlist.
watchlist = ["RELIANCE", "TCS", "INFY"]

watchlist.append("HDFCBANK")     # add to the end
watchlist.insert(0, "NIFTY")     # add at a specific position (the front)
print("After adding :", watchlist)

watchlist.remove("TCS")          # remove the first matching value
last = watchlist.pop()           # remove AND return the last item
print("Popped off   :", last)
print("Final list   :", watchlist)
```

Live output

```
After adding : ['NIFTY', 'RELIANCE', 'TCS', 'INFY', 'HDFCBANK']
Popped off   : HDFCBANK
Final list   : ['NIFTY', 'RELIANCE', 'INFY']
```

RELIANCE TCS INFY HDFCBANK .append() adds here .pop() removes from here append() adds to the end; pop() takes from the end. insert() and remove() handle any position.
The four you'll use most: **`append`**adds to the end,**`insert`**drops an item at a chosen position,**`remove`**deletes by value, and**`pop`**removes the last item _and hands it back_ to you. A list is a living thing - it remembers every change.
Key idea
A **list** `[a, b, c]` holds ordered values you can index and slice like a string - but unlike a string, a list is **mutable** : `append`, `insert`, `remove` and `pop` change it in place.
## Instant insight: max, min, sum and sorting
Hand a list of numbers to Python's built-in helpers and you get analysis for free:
EX 3High, low, average, and two ways to sortPYch09/03_methods_sorting.py
Copy
```
# Built-in helpers turn a list of numbers into instant insight.
closes = [101.2, 103.5, 102.8, 104.1, 105.6, 104.9, 106.3]

print("Highest close:", max(closes))
print("Lowest close :", min(closes))
print("Average close:", round(sum(closes) / len(closes), 2))

# sorted() returns a NEW sorted list and leaves the original untouched.
print("Sorted (asc) :", sorted(closes))
print("Original kept:", closes)

# .sort() rearranges the list IN PLACE - it changes the original.
closes.sort(reverse=True)
print("Sorted (desc):", closes)
```

Live output

```
Highest close: 106.3
Lowest close : 101.2
Average close: 104.06
Sorted (asc) : [101.2, 102.8, 103.5, 104.1, 104.9, 105.6, 106.3]
Original kept: [101.2, 103.5, 102.8, 104.1, 105.6, 104.9, 106.3]
Sorted (desc): [106.3, 105.6, 104.9, 104.1, 103.5, 102.8, 101.2]
```

`max`, `min`, `sum` and `len` answer the obvious questions in one word each - there's your week's high, low and average. Sorting, though, hides a trap worth flagging:
Tip
There are **two ways to sort** , and they behave differently. **`sorted(closes)`**returns a _brand-new_ sorted list and leaves the original alone. **`closes.sort()`**rearranges the original list _in place_ and returns nothing. Reach for `sorted()` when you want to keep the original order (you usually do); use `.sort()` only when you truly want to overwrite it.
Did you know?
**Instagram runs on Python.** The app that serves photos and reels to hundreds of millions of people every day is built on Python (using the Django web framework) - one of the largest Python deployments on the planet. The everyday lists, dictionaries and loops you're learning now are the very same building blocks holding up apps at that scale.
## A list can hold anything
One last superpower: a Python list isn't fussy about what goes inside. It can mix types - numbers, text, even other lists:

```
bar = ["RELIANCE", 1300.0, 1313.6, 50]      # symbol, open, close, qty
table = [["RELIANCE", 1313.6], ["TCS", 2109.0]]   # a list of rows

```

That second example - a _list of lists_ - is secretly a little table, with each inner list a row. Hold that thought: it's exactly how spreadsheets and DataFrames are organised, and we'll meet it again in Module 4.
## Try it yourself
  * From the `closes` list, slice out just the **middle three** days and find their average.
  * Start an empty watchlist with `wl = []`, then `append` three symbols of your choice and print the result.
  * Run `sorted(closes)` and then print `closes` right after. Confirm for yourself that the original is unchanged - then do the same with `.sort()` and watch the difference.


## Recap
  * A **list** `[...]` stores **ordered** values; index and slice it exactly like a string.
  * Lists are **mutable** : **`append`**(add to end),**`insert`**(add at position),**`remove`**(by value),**`pop`**(take the last).
  * Built-ins **`max`/`min` / `sum` / `len`** summarise a list instantly.
  * **`sorted()`**returns a new sorted list;**`.sort()`**reorders in place - know which you want.
  * A list can hold **mixed types** , and a **list of lists** is a table in disguise.


Lists are flexible because they can change. But sometimes you want the _opposite_ - a small group of values that's locked and can't be altered by accident, like the four numbers of an OHLC bar. For that, Python gives us the **tuple** - the subject of the next chapter.
On this page
