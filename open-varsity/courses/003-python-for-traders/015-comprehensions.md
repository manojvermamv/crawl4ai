Chapters
Module 2 · Core Programming - Chapter 15
# Comprehensions
The elegant Python one-liner that builds a new list or dict from an old one - you'll see it everywhere.
PY
What you'll learn
  * ·List comprehensions
  * ·Filtering with if
  * ·Transforming prices
  * ·Dict comprehensions
  * ·Readability vs cleverness
  * ·Common patterns


In the last chapter you wrote a loop that built a new list: start with an empty list, loop over something, `append` a transformed value each time. That pattern - _make a new list from an old one_ - is so common that Python gives you a beautiful one-line shorthand for it: the **comprehension**. Once it clicks, you'll read and write it everywhere, and your code will get noticeably shorter and clearer. It looks strange for about five minutes, then it looks obvious.
## The list comprehension
Here's the same job done twice - the familiar loop, and the comprehension that replaces it:
EX 1A loop and its one-line comprehension - identical resultsPYch15/01_list_comprehension.py
Copy
```
symbols = ["RELIANCE", "TCS", "INFY", "HDFCBANK"]

# The long way: a loop that builds a new list item by item.
yahoo = []
for s in symbols:
    yahoo.append(s + ".NS")

# The comprehension way: the exact same result, in one readable line.
yahoo_quick = [s + ".NS" for s in symbols]

print("Loop         :", yahoo)
print("Comprehension:", yahoo_quick)
print("Identical?   :", yahoo == yahoo_quick)
```

Live output

```
Loop         : ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS']
Comprehension: ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS']
Identical?   : True
```

Both build `['RELIANCE.NS', 'TCS.NS', ...]`; the `Identical? True` proves it. The comprehension `[s + ".NS" for s in symbols]` reads right out of the loop: _the value to collect_ (`s + ".NS"`) comes first, then _the loop_ (`for s in symbols`). Picture it like this:
[ price * 1.05 for price in closes if price > 100 ] the value to collect - transform each item the loop - visit every item in turn the filter - keep only items that pass (optional) A comprehension: what to keep, the loop, and an optional filter - all on one line.
Key idea
A **list comprehension** `[expression for item in collection]` builds a new list in one line. The **expression** (what to collect) comes first, then the **`for`**loop. It's the compact form of "make an empty list and append in a loop."
## Filtering with if
Tack an **`if`**onto the end and the comprehension keeps only the items that pass - filtering and transforming in a single, readable stroke:
EX 2Filtering, and filtering-plus-transforming, in one linePYch15/02_filter.py
Copy
```
closes = [101.2, 103.5, 99.8, 104.1, 98.5, 106.3]

# Add an "if" to the end to KEEP only the items that pass a test.
above_100 = [c for c in closes if c > 100]
print("Above 100:", above_100)

# Transform AND filter together: round only the prices above 104.
strong = [round(c, 1) for c in closes if c > 104]
print("Strong   :", strong)
```

Live output

```
Above 100: [101.2, 103.5, 104.1, 106.3]
Strong   : [104.1, 106.3]
```

The first line keeps prices above 100; the second rounds _only_ the prices above 104. Read it left to right as a sentence: "round c, for each c in closes, if c is above 104." That ordering - value, loop, filter - is always the same.
## Dict comprehensions
The same idea builds dictionaries too, with curly braces and a `key: value` expression. Paired with **`zip()`**- which stitches two lists together - it's the tidiest way to turn parallel lists into a lookup:
EX 3Building a quote dictionary with zip and a comprehensionPYch15/03_dict_comprehension.py
Copy
```
symbols = ["RELIANCE", "TCS", "INFY"]
prices = [1313.60, 2109.00, 1056.60]

# zip() pairs the two lists; the dict comprehension builds {symbol: price}.
quotes = {sym: price for sym, price in zip(symbols, prices)}

print("Quotes:", quotes)
print("TCS   :", quotes["TCS"])
```

Live output

```
Quotes: {'RELIANCE': 1313.6, 'TCS': 2109.0, 'INFY': 1056.6}
TCS   : 2109.0
```

`zip(symbols, prices)` walks the two lists in lockstep, handing out `("RELIANCE", 1313.60)`, `("TCS", 2109.00)`, and so on, which the comprehension turns straight into `{symbol: price}`. You'll use this exact move to assemble lookups from data all the time.
Did you know?
**Comprehensions come from mathematics.** That set-builder notation you may have met in school - { 2x | x is in S } , "the set of 2x for every x in S" - is almost exactly Python's `[2 * x for x in S]`. Python borrowed the idea from functional languages like Haskell, which borrowed it from maths itself. So when a comprehension feels strangely natural, it's because you've quietly seen its shape before.
## Readability over cleverness
A word of caution, because comprehensions are seductive. They shine for **simple, single-thought** transforms and filters. But you _can_ cram loops-within-loops and tangled logic into one, and the result becomes a write-only puzzle nobody (including you, next week) can read.
Tip
The test is one breath: if you can say what a comprehension does in a single short sentence, it's a good comprehension. If explaining it needs "and then, but only when, unless..." - stop, and write it as an ordinary `for` loop with an `if`. Clear beats clever every time; remember the Zen of Python from Chapter 4.
## Try it yourself
  * Turn `[1313.6, 2109.0, 1056.6]` into a list of those prices rounded to whole rupees, using a comprehension.
  * From `closes = [101.2, 103.5, 99.8, 104.1, 98.5]`, build a list of just the _down_ days (below 100).
  * Build a dict comprehension that maps each symbol in `["RELIANCE", "TCS"]` to its length in characters. (Hint: `{s: len(s) for s in ...}`.)


## Recap
  * A **comprehension** builds a new collection in one line: `[expression for item in collection]`.
  * Read it as **value, then loop, then optional filter** ; add **`if`**at the end to keep only matching items.
  * **Dict comprehensions** (`{k: v for ...}`) build dictionaries, often paired with **`zip()`**to combine parallel lists.
  * Favour **readability** : use comprehensions for simple transforms/filters, and fall back to a plain loop when the logic gets complicated.


You've now met data structures, decisions, loops and comprehensions - you can express almost any small piece of logic. The final building block of Module 2 is the one that lets you _name_ a piece of logic and reuse it forever, instead of copying it around: the **function**. It's next, and it's a big one.
On this page
