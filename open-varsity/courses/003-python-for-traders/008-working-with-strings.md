Chapters
Module 1 · Getting Started with Python - Chapter 08
# Working with Strings
Symbols, tickers and dates are all text. Slice them, clean them and reshape them with Python's string toolkit.
PYNSE
What you'll learn
  * ·Strings as text
  * ·Indexing & slicing
  * ·Upper, lower & strip
  * ·split & join
  * ·Checking & replacing
  * ·Building ticker strings


Look around a trading screen and you'll see text everywhere: symbols like RELIANCE, exchange codes like NSE, dates like 2026-06-25, order types, news headlines. To a computer all of this is one type - the **string** - and learning to slice, clean and reshape strings is a genuinely useful everyday skill. Data almost never arrives in the exact shape you want; strings are how you fix that. This chapter rounds off the basics, and it's a practical one.
## A string is a sequence of characters
A string is just characters in a row, and each character has a **position** - an _index_ - starting at `0`. Square brackets reach in by position, and a colon inside them takes a **slice** (a range):
EX 1Reaching into a string by position and slicePYch08/01_indexing_slicing.py
Copy
```
# A string is a sequence of characters - reach in by position with [ ].
symbol = "RELIANCE"

print("First letter:", symbol[0])     # R  - counting starts at 0
print("Last letter :", symbol[-1])    # E  - negative counts from the end
print("First three :", symbol[:3])    # REL - a "slice" from start up to 3
print("Length      :", len(symbol))   # 8  - how many characters

# Slicing is a quick way to pull pieces out of a date string.
date = "2026-06-25"
print("Year :", date[:4])             # 2026
print("Month:", date[5:7])            # 06
print("Day  :", date[8:])             # 25
```

Live output

```
First letter: R
Last letter : E
First three : REL
Length      : 8
Year : 2026
Month: 06
Day  : 25
```

The two ideas that trip people up are _zero-based_ counting and _negative_ indexing. Picture the word laid out with its index numbers:
0R-8 1E-7 2L-6 3I-5 4A-4 5N-3 6C-2 7E-1 Index from the front (0, blue) or the back (-1, purple). A slice [:3] takes positions 0, 1, 2.
So `symbol[0]` is `R`, `symbol[-1]` is the last `E`, and the slice `symbol[:3]` grabs `REL` - it stops _just before_ index 3. That "up to, but not including" rule is everywhere in Python, so it's worth fixing in your mind now.
Key idea
Strings are **indexed from 0** ; negative indices count from the end (`-1` is last). A **slice** `text[start:stop]` includes `start` but stops _just before_ `stop`. Leave a side blank to go to the very beginning or end.
## Cleaning and checking text
Real data is messy - stray spaces, mixed case, codes glued together. String **methods** , attached with a dot, tidy it up. Here are the ones you'll use weekly:
EX 2Cleaning with strip/upper, checking, and replacingPYch08/02_methods.py
Copy
```
# Messy text in, tidy text out. Methods are attached with a dot.
raw = "  reliance  "
clean = raw.strip().upper()           # strip removes outer spaces, upper capitalises
print("Cleaned:", repr(clean))        # repr shows the quotes, proving spaces are gone

# Checking what a string contains.
symbol = "NSE:RELIANCE"
print("Starts with NSE? ", symbol.startswith("NSE"))   # True
print("Contains a colon?", ":" in symbol)              # True

# Replacing part of a string (it returns a NEW string).
print("Swap exchange   :", symbol.replace("NSE", "BSE"))  # BSE:RELIANCE
```

Live output

```
Cleaned: 'RELIANCE'
Starts with NSE?  True
Contains a colon? True
Swap exchange   : BSE:RELIANCE
```

`strip()` shaves off surrounding spaces, `upper()`/`lower()` fix the case, `startswith()` and the `in` keyword check contents, and `replace()` swaps text out. Notice we _reassigned_ the result - because of an important quirk:
Tip
**Strings are immutable** - you can't change one in place. Methods like `upper()` and `replace()` don't edit the original; they hand you a **brand-new string**. So you must capture it: `clean = raw.strip().upper()`. Writing `raw.strip()` on its own and expecting `raw` to change is a classic beginner slip.
## Splitting and joining
Two methods are a matched pair and worth memorising together. `split()` breaks a string into a **list** of pieces; `join()` glues a list of strings back into one. They're how you read and write the comma-separated data you'll meet constantly:
EX 3split() text into a list, join() a list into textPYch08/03_split_join.py
Copy
```
# split() breaks text into a list; join() glues a list back into text.
line = "RELIANCE,TCS,INFY,HDFCBANK"
symbols = line.split(",")             # split on each comma

print("Symbols list:", symbols)
print("Count       :", len(symbols))
print("Third symbol:", symbols[2])    # INFY

# join() is split's mirror image - here with " | " between items.
print("Joined      :", " | ".join(symbols))

# Building a Yahoo Finance ticker by adding the .NS suffix (a taste of Chapter 34).
nse_symbol = "RELIANCE"
print("Yahoo ticker:", nse_symbol + ".NS")
```

Live output

```
Symbols list: ['RELIANCE', 'TCS', 'INFY', 'HDFCBANK']
Count       : 4
Third symbol: INFY
Joined      : RELIANCE | TCS | INFY | HDFCBANK
Yahoo ticker: RELIANCE.NS
```

We split `"RELIANCE,TCS,INFY,HDFCBANK"` on the comma to get four separate symbols, then joined them back with `" | "`. (Don't worry about lists yet - that's literally the next chapter.) And building a Yahoo Finance ticker is just sticking `.NS` on the end, a small taste of the symbol systems we'll untangle in Chapter 34.
Did you know?
**Every Python 3 string is Unicode.** That means a string can hold text in _any_ writing system on Earth - English, Hindi (रिलायंस), Tamil, Bengali, Chinese - and even emoji, all natively, no special handling. For Indian markets, where company names and news arrive in many languages and scripts, this is quietly a very big deal: to Python, `"रिलायंस"` is just as ordinary a string as `"RELIANCE"`.
## Try it yourself
  * From the string `"2026-06-25"`, use slicing to print it in `DD-MM-YYYY` order: `25-06-2026`. (Combine three slices with `+`.)
  * Take `"  nse:tcs  "` and turn it into the clean, uppercase `"NSE:TCS"` in a single chained line of methods.
  * Split the sentence `"buy 50 RELIANCE"` on spaces. What's at index `1`, and what type is it - could you multiply it yet?


## Recap
  * A **string** is a sequence of characters, indexed from **0** ; **negative** indices count from the end.
  * A **slice** `text[start:stop]` includes `start` and stops just before `stop`.
  * Methods clean and inspect text - **`strip``upper` `lower` `replace`**, **`startswith`**, and**`in`**- but strings are**immutable** , so they return _new_ strings.
  * **`split()`**turns text into a list and**`join()`**turns a list back into text - the everyday tools for comma-separated data.


That wraps up **Module 1** - you can install Python, run code, store and convert values, calculate, format output, and handle text. You officially know the basics. In **Module 2** we level up to the structures that hold _many_ values at once, starting with the most important one of all: the **list** , perfect for a whole series of prices.
On this page
