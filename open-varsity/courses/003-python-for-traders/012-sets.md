Chapters
Module 2 · Core Programming - Chapter 12
# Sets
A bag of unique things. Strip duplicate symbols, test membership instantly, and compare two watchlists with set maths.
PY
What you'll learn
  * ·What a set is
  * ·Removing duplicates
  * ·Fast membership tests
  * ·Union & intersection
  * ·Two-watchlist overlap
  * ·Set vs list


Here's a question that comes up all the time in trading: "How many _different_ stocks did I trade today?" or "Which names are on _both_ my watchlist and my friend's?" You could answer these with lists and a lot of fiddly checking - or you could use the tool built exactly for uniqueness and membership: the **set**. It's the last of the four core collections, it's quick to learn, and for the right job it's wonderfully clean.
## A set: unique things, no order
A set holds only **unique** items - feed it duplicates and they quietly collapse into one. The fastest way to make one is to hand `set()` a list:
EX 1Deduplicating trades and testing membershipPYch12/01_set_basics.py
Copy
```
# A set holds only UNIQUE items - duplicates simply vanish.
trades = ["RELIANCE", "TCS", "RELIANCE", "INFY", "TCS", "RELIANCE"]
unique = set(trades)                  # turn the list into a set

print("Raw trades   :", len(trades))            # 6 trades...
print("Unique count :", len(unique))            # ...in only 3 names
print("Unique names :", sorted(unique))         # a set has no order, so we sort to print

# Membership tests on a set are instant - ideal for "have I seen this?"
print("Traded INFY? ", "INFY" in unique)        # True
print("Traded HDFC? ", "HDFCBANK" in unique)    # False
```

Live output

```
Raw trades   : 6
Unique count : 3
Unique names : ['INFY', 'RELIANCE', 'TCS']
Traded INFY?  True
Traded HDFC?  False
```

Six trades became three unique names, with zero effort. And notice the `in` test: checking whether something is in a set is **instant** , however large the set grows - the same hash-table magic that makes dictionaries fast. A set is unordered, though, so there's no `[0]` and no guaranteed sequence; that's why we wrap it in `sorted()` purely to print it tidily.
Heads up
**An empty set is written`set()` , not `{}`.** Curly braces with nothing inside make an empty _dictionary_ , not a set - a genuinely confusing quirk that catches everyone once. Need an empty set to start filling? Write `seen = set()`.
## The maths of overlap
Sets really earn their place when you compare two of them. Python borrows the actual symbols of mathematical set theory, and they read beautifully:
EX 2Intersection, union and difference of two watchlistsPYch12/02_set_operations.py
Copy
```
# Two watchlists, compared with real set maths.
mine = {"RELIANCE", "TCS", "INFY", "HDFCBANK"}
friend = {"INFY", "HDFCBANK", "ITC", "SBIN"}

print("In both (intersection):", sorted(mine & friend))   # &  shared by both
print("Either list (union)   :", sorted(mine | friend))   # |  everything, once
print("Only mine (difference):", sorted(mine - friend))   # -  in mine, not theirs
```

Live output

```
In both (intersection): ['HDFCBANK', 'INFY']
Either list (union)   : ['HDFCBANK', 'INFY', 'ITC', 'RELIANCE', 'SBIN', 'TCS']
Only mine (difference): ['RELIANCE', 'TCS']
```

My watchlist Friend's RELIANCE TCS INFY HDFCBANK ITC SBIN & = the shared middle | | = both circles | - = only the left Intersection is the overlap, union is everything, difference is what's left when you subtract.
The picture says it all: **`&`intersection** is the overlap (`INFY`, `HDFCBANK`), **`|`union** is both circles combined (every name, once), and **`-`difference** is your circle with the shared part removed (`RELIANCE`, `TCS`). One symbol each, no loops, no fuss.
Key idea
A **set** `{a, b, c}` holds **unique, unordered** items with instant **`in`**tests. Compare sets with**`&`**(shared),**`|`**(combined) and**`-`**(only in the first). Make an empty one with`set()`.
Did you know?
**Spotify runs on Python.** The streaming service uses Python across its backend and, especially, the data work behind recommendations - the engine that builds your Discover Weekly by finding the _overlap_ between your taste and millions of others'. That's the very same set-overlap thinking you just used to compare two watchlists, only at planetary scale.
## Set or list - which should I use?
They're not rivals; they're for different jobs:
  * Use a **list** when **order matters** , duplicates are allowed, or you need to reach items by position (a price series, today's trades in sequence).
  * Use a **set** when you only care about **uniqueness or membership** - "is this symbol in my universe?", "how many distinct names?", "what's shared between these two groups?"


Tip
A neat trick you'll reuse: to strip duplicates from a list while you don't care about order, just wrap it - `set(my_list)`. And to get a clean, duplicate-free, _ordered_ result, combine the two ideas: `sorted(set(my_list))`.
## Try it yourself
  * Turn the list `["NIFTY", "BANKNIFTY", "NIFTY", "FINNIFTY"]` into a set and print how many unique index names it holds.
  * Given `large = {"RELIANCE", "TCS", "INFY"}` and `fno = {"TCS", "SBIN"}`, find which of your stocks are _also_ in the F&O set using `&`.
  * Use `-` to find the names in `large` that are **not** in `fno`.


## Recap
  * A **set** `{...}` stores **unique, unordered** items; `set(a_list)` instantly removes duplicates.
  * Membership (**`in`**) is fast at any size; there's no order and no indexing.
  * Compare sets with **`&`**(intersection),**`|`**(union) and**`-`**(difference).
  * An **empty set is`set()`** - `{}` is an empty dictionary.
  * Use a **list** for ordered, possibly-repeated data; a **set** for uniqueness and membership.


That completes your toolkit of containers: **lists, tuples, dictionaries and sets**. You can now store data in every shape you'll meet. The next step is to make your programs _decide_ what to do with that data - to act only when a condition is met. In the next chapter we wire up the **`if`statement** , and your code starts making choices.
On this page
