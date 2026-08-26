Chapters
Module 1 · Getting Started with Python - Chapter 07
# Input, Output & f-strings
Print results clearly and read input - and format rupees, dollars and percentages so they actually look right.
PY
What you'll learn
  * ·The print() function
  * ·Reading input()
  * ·f-strings explained
  * ·Formatting money & %
  * ·Rounding in output
  * ·Multi-line output


So far our programs have done their work in silence and shown a few rough numbers. Real tools _communicate_ - they print clean, readable results, and sometimes they ask the user a question. In this chapter we'll polish how Python talks back to you with **`print()`**, meet the wonderful**f-string** for formatting money and percentages exactly the way you want, and learn to read input with **`input()`**. This is the chapter that makes your output look professional.
## print(), properly
You've used `print()` since Chapter 2, but it has a few handy tricks. It happily takes several values at once, and two little settings - `sep` and `end` - control the spaces between them and how the line finishes:
EX 1print() with several values, sep, end and multi-line textPYch07/01_printing.py
Copy
```
# print() can take several values at once, separated by spaces by default.
symbol = "RELIANCE"
price = 1313.60
print("Symbol:", symbol, "Price:", price)

# sep= changes what goes BETWEEN values; end= changes how the line ENDS.
print("NSE", "RELIANCE", "1313.60", sep=" | ")
print("Loading", end="...")
print("done")

# Triple quotes make a multi-line block that prints exactly as written.
report = """--- Position ---
Symbol : RELIANCE
Shares : 50"""
print(report)
```

Live output

```
Symbol: RELIANCE Price: 1313.6
NSE | RELIANCE | 1313.60
Loading...done
--- Position ---
Symbol : RELIANCE
Shares : 50
```

Three things to notice: `print()` puts a space between values by default (`sep` changes that to `|`); `end="..."` stops it moving to a new line, so the next `print` continues on the same one; and **triple-quoted** text (`"""..."""`) lets you write a whole block exactly as it should appear, newlines and all.
## f-strings: the clean way to build text
Gluing variables into a message with commas works, but it's clumsy. The modern, readable way is the **f-string** : put the letter `f` right before the opening quote, and then drop any variable - or even a calculation - straight into the text inside curly braces `{ }`:
EX 2f-strings, with formatting for money, signs and percentagesPYch07/02_fstrings.py
Copy
```
# An f-string starts with the letter f and drops values straight into { }.
symbol = "RELIANCE"
qty = 50
price = 1313.60
buy = 1300.00

print(f"{symbol}: {qty} shares at {price}")

# After a colon comes a "format spec" that controls how a number looks.
print(f"Value      : {qty * price:,.2f}")          # thousands comma + 2 decimals
print(f"Change     : {price - buy:+.2f}")          # always show the + or - sign
print(f"Return     : {(price - buy) / buy:.2%}")   # display as a percentage
print(f"Price (0dp): {price:.0f}")                 # round to a whole number
```

Live output

```
RELIANCE: 50 shares at 1313.6
Value      : 65,680.00
Change     : +13.60
Return     : 1.05%
Price (0dp): 1314
```

The magic is what comes _after the colon_ inside the braces - the **format spec**. It turns a raw number into something a human wants to read:
f"Value: {qty * price:,.2f}" becomes Value: 65,680.00 f marks the text as an f-string { qty * price } a value or calculation goes here :,.2f how to format it - thousands comma, 2 decimals An f-string: the f, the value in braces, and the format spec after the colon.
A few specs you'll use constantly, all visible in the output above:
  * **`:,.2f`**- a comma every thousand and 2 decimal places:`65,680.00`. Perfect for money.
  * **`:+.2f`**- always show the sign:`+13.60` (or `-13.60` for a loss). Great for changes.
  * **`:.2%`**- multiply by 100 and add a`%` sign: `1.05%`. Made for returns.
  * **`:.0f`**- round to a whole number:`1314`.


Key idea
An **f-string** is `f"...{value}..."`. Put any variable or calculation in the braces, and after a colon add a **format spec** (`,.2f` for money, `+.2f` for signed, `.2%` for percent). It's the cleanest way to turn numbers into readable output.
## Aligning into clean tables
Numbers that don't line up are painful to read. Add an **alignment** marker and a **width** to the spec, and ragged output snaps into neat columns - the difference between a wall of digits and a readable watchlist:
EX 3Building a column-aligned tablePYch07/04_alignment.py
Copy
```
# Alignment and width turn ragged output into a clean, column-aligned table.
rows = [
    ("RELIANCE", 1313.60, 1.05),
    ("TCS", 2109.00, -0.52),
    ("INFY", 1056.60, 0.63),
]

# <  left-align   >  right-align   ^  centre   - then a width number.
print(f"{'Symbol':<10}{'LTP':>10}{'Chg%':>8}")
print("-" * 28)
for sym, ltp, chg in rows:
    print(f"{sym:<10}{ltp:>10.2f}{chg:>+8.2f}")

# A fill character goes before the alignment - here, pad with dots.
print()
print(f"{'TOTAL':.<20}{4479.20:>8.2f}")
```

Live output

```
Symbol           LTP    Chg%
----------------------------
RELIANCE     1313.60   +1.05
TCS          2109.00   -0.52
INFY         1056.60   +0.63

TOTAL............... 4479.20
```

The three alignment markers are **`<`**(left),**`>`**(right) and**`^`**(centre), each followed by the column width. Numbers read best**right-aligned** (`>`) so their decimal points line up; text reads best **left-aligned** (`<`). You can even set a **fill character** before the alignment - `:.<20` pads with dots instead of spaces, the classic "dotted leader" for a totals line. This one trick turns f-strings into a tool for printing clean P&L tables, reports and watchlists.
Tip
A reliable recipe for a table: left-align the label column (`{sym:<10}`) and right-align each number column with a matching width and decimals (`{ltp:>10.2f}`). Once every column has a fixed width, the rows line up into a perfect grid no matter what the values are.
## More formatting power
A few more specifiers come up constantly in trading code:
EX 4The = debugger, dates, padding and dynamic widthsPYch07/05_advanced.py
Copy
```
from datetime import datetime

price = 1313.60
qty = 50

# The = specifier prints "expression=value" - brilliant for quick debugging.
print(f"{price=}")
print(f"{qty * price=:,.2f}")

# Dates format right inside an f-string, using strftime codes after the colon.
now = datetime(2026, 6, 25, 15, 30)
print(f"As of {now:%d %b %Y, %H:%M}")

# Leading zeros for fixed-width codes (an order id, a strike, a token).
order_id = 42
print(f"Order #{order_id:05d}")

# The width itself can come from a variable - nest braces inside the spec.
width = 12
print(f"{'Padded':>{width}}|")
```

Live output

```
price=1313.6
qty * price=65,680.00
As of 25 Jun 2026, 15:30
Order #00042
      Padded|
```

  * **The`=` specifier** - `f"{price=}"` prints `price=1313.6`, echoing the expression _and_ its value. It's the fastest debugging tool in Python (you'll lean on it in Chapter 20), and it still honours a format spec: `f"{qty * price=:,.2f}"`.
  * **Dates** format right inside the braces - `f"{now:%d %b %Y, %H:%M}"` uses the same `%` codes from Chapter 23, with no separate `strftime` call.
  * **Leading zeros** - `f"{order_id:05d}"` zero-pads an integer to width 5 (`00042`), ideal for fixed-width ids, tokens and strikes.
  * **Dynamic widths** - the width itself can be a variable: `f"{text:>{width}}"`. Nest the braces and the spec is built on the fly.


## The format-spec cheat-sheet
Everything after the colon follows one mini-language: **`{value:[fill][align][sign][width][,][.precision][type]}`**. You'll rarely use all of it at once, but here's the part a trader reaches for:
  * **Decimals:** `:.2f` two - `:.4f` four - `:.0f` none.
  * **Thousands:** `:,` grouping - `:,.2f` grouped with 2 decimals (`65,680.00`).
  * **Percent:** `:.2%` multiplies by 100 and adds `%` (`1.05%`).
  * **Sign:** `:+.2f` always shows `+`/`-`; `: .2f` (a space) leaves room so positives align under negatives.
  * **Align & width:** `:<10` left - `:>10` right - `:^10` centre.
  * **Fill:** `:*>10` pad with `*` - `:.<20` pad with dots.
  * **Leading zeros:** `:05d` zero-pad an integer to width 5.
  * **Dates:** `:%Y-%m-%d` (any strftime codes).
  * **Conversions:** `!r` shows the `repr` (with quotes), `!s` the `str`, and `=` echoes the expression for debugging.


Bookmark this: between these specifiers you can format almost anything a trading screen needs to display.
## Reading input from the user
To ask the user a question, use **`input()`**. It prints your prompt, waits for them to type and press Enter, and hands back what they typed. There's one rule you must never forget - and Chapter 5 already warned you about it:
EX 5input() always returns text - convert before doing mathsPYch07/03_input.py
Copy
```
# input() pauses and waits for the user to type, then returns what they typed.
# IMPORTANT: it always returns TEXT (a str), even when they type digits.
quantity_text = input("How many shares do you hold? ")
quantity = int(quantity_text)          # convert text -> number before any maths

price = 1313.60
print()
print(f"You typed {quantity_text!r}, which is a {type(quantity_text).__name__}.")
print(f"As a number that is {quantity}.")
print(f"Position value: {quantity * price:,.2f}")
```

Live output

```
How many shares do you hold? 
You typed '50', which is a str.
As a number that is 50.
Position value: 65,680.00
```

See it plainly in the output: even though the user typed digits, `input()` returned the **text** `'50'` (a `str`), not the number `50`. We had to run it through `int()` before multiplying. Forget that step and `quantity * price` would either error or do something bizarre.
Heads up
**`input()`always returns a`str`** - always. Before you do any arithmetic with it, convert it with `int()` or `float()`. This single oversight is behind a huge share of beginner bugs, so make the conversion a reflex.
Did you know?
**Python is the world's most popular language for teaching people to code.** A widely cited 2014 study found Python had overtaken Java as the top introductory teaching language at most leading US universities - and it's only grown since. A big reason is exactly what this chapter is about: a beginner's first program is a single, readable line, `print("Hello, World!")`, where other languages demand a screenful of ceremony first.
## Try it yourself
  * Change the f-string `{qty * price:,.2f}` to `{qty * price:,.0f}`. How does the displayed value change, and why might "no decimals" suit large rupee figures?
  * Build one f-string that prints: `RELIANCE up +1.05% today`, using the variables from the second example.
  * Run `03_input.py` yourself in a terminal and actually type a number. Then type a word like `fifty` instead - what kind of error appears? (We'll learn to handle that gracefully in Chapter 20.)


## Recap
  * **`print()`**takes multiple values; tune it with**`sep`**(separator) and**`end`**(line ending), and use**triple quotes** for multi-line text.
  * **f-strings** (`f"...{value}..."`) drop variables and calculations straight into text.
  * A **format spec** after the colon shapes numbers: **`,.2f`**money,**`+.2f`**signed,**`.2%`**percent,**`.0f`**whole.
  * **Alignment** (`<` `>` `^`) plus a **width** builds clean tables; a **fill** char (`:.<20`) makes dotted-leader totals.
  * More power: the **`=`**debug specifier (`f"{price=}"`), **dates** in braces (`f"{now:%d %b %Y}"`), **leading zeros** (`:05d`), and **dynamic widths** (`{x:>{w}}`).
  * **`input()`**reads from the user but**always returns a`str`** - convert with `int()`/`float()` before any maths.


You've now noticed something: text - strings - keeps showing up everywhere, from symbols to prompts to formatted output. It's time to give strings their full due. In the next chapter we'll slice, clean and reshape text, the raw material of every ticker, date and label you'll handle.
On this page
