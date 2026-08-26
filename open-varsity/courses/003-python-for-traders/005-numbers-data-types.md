Chapters
Module 1 · Getting Started with Python - Chapter 05
# Numbers & Data Types
Integers, decimals, text and true/false - the basic kinds of data, and how to turn one into another.
PY
What you'll learn
  * ·int, float, str, bool
  * ·The type() function
  * ·Whole numbers vs decimals
  * ·Converting between types
  * ·Rounding money correctly
  * ·Truthy values


In the last chapter you stored a price, a symbol and a quantity in variables - and you might not have noticed that those three values are fundamentally _different kinds of thing_. A quantity is a whole number. A price has a decimal. A symbol is text. And "is the market open?" is a simple yes or no. Python cares deeply about these differences, because what you can _do_ with a value depends on its **type**. Get comfortable with the handful of basic types now, and a whole category of confusing bugs will simply never happen to you.
## Four kinds of value
Almost everything you'll handle as a beginner is one of four types:
EX 1The four everyday types, revealed by type()PYch05/01_four_types.py
Copy
```
# Python's four everyday data types, one per piece of a trade.
quantity = 50            # int   - a whole number
price = 1313.60          # float - a number with a decimal point
symbol = "RELIANCE"      # str   - text, always in quotes
is_market_open = True    # bool  - either True or False

# type() tells you what kind of value something is.
print(quantity, "->", type(quantity))
print(price, "->", type(price))
print(symbol, "->", type(symbol))
print(is_market_open, "->", type(is_market_open))
```

Live output

```
50 -> <class 'int'>
1313.6 -> <class 'float'>
RELIANCE -> <class 'str'>
True -> <class 'bool'>
```

The `type()` function is your truth-teller: hand it any value and it tells you exactly what kind it is. Here's the cast:
int 50 whole number float 1313.60 decimal str "RELIANCE" text bool True yes or no int, float, str and bool - the four types you'll meet on day one.
Key idea
**int** is a whole number (`50`), **float** is a number with a decimal point (`1313.60`), **str** is text in quotes (`"RELIANCE"`), and **bool** is either `True` or `False`. Use `type(value)` whenever you're unsure what you're holding.
## Whole numbers vs decimals
The split between `int` and `float` matters in trading. Counts are whole: you hold **50 shares** , you trade **2 lots** - those are `int`s. Measured things carry decimals: a **price** of 1313.60, a **return** of 1.45% - those are `float`s.
One small surprise: dividing two whole numbers in Python gives you a `float`, even when it divides evenly. `100 / 4` is `25.0`, not `25` - the decimal point shows up the moment division enters. That's usually exactly what you want with money.
Did you know?
**Python's whole numbers have no size limit.** In most languages an integer overflows and breaks once it passes about 9 quintillion (2 to the power 63). Python just keeps going - ask it for `2 ** 1000` and it prints all 302 digits, no errors, no special tricks. For finance, where a careless overflow could mean a very wrong number, that quiet reliability is a real gift.
## Converting between types
You'll constantly need to turn one type into another, and the tools are named after the types themselves: `int()`, `float()`, and `str()`. The classic trap - the one that catches _everybody_ once - is text that merely _looks_ like a number:
EX 2Converting types, and the text-vs-number trapPYch05/02_converting.py
Copy
```
# 1) Text vs number: the same "* 3" behaves very differently.
shares_text = "50"                 # this is TEXT, not a number
shares = int(shares_text)          # convert the text into a whole number
print('"50" * 3 gives:', shares_text * 3)   # text just repeats
print(" 50  * 3 gives:", shares * 3)         # real arithmetic

# 2) Rounding money to two decimal places.
gross = 1313.60 * 1.07             # add 7 percent
print("Before rounding:", gross)
print("Rounded to 2dp :", round(gross, 2))

# 3) A famous floating-point surprise - decimals are not always exact.
print("0.1 + 0.2 =", 0.1 + 0.2)
```

Live output

```
"50" * 3 gives: 505050
 50  * 3 gives: 150
Before rounding: 1405.552
Rounded to 2dp : 1405.55
0.1 + 0.2 = 0.30000000000000004
```

Look closely at the first two lines of output. `"50" * 3` gives `505050` - because `"50"` is **text** , and multiplying text repeats it. Only after `int("50")` turns it into the number `50` does `* 3` give the `150` you expected. This matters because data often arrives as text - from a file, a webpage, or the keyboard - and you must convert it before doing maths.
Note
When you read input from the user (Chapter 7) or a file (Chapter 21), it arrives as a **`str`**- always. Forgetting to convert it to a number before calculating is one of the most common beginner bugs. Now you know to watch for it.
## Rounding money (and a famous surprise)
The same example shows two more essentials. `round(gross, 2)` rounds a value to 2 decimal places - perfect for displaying rupees and paise, or dollars and cents. And then there's the eyebrow-raiser: `0.1 + 0.2` comes out as `0.30000000000000004`, not `0.3`.
That's not a Python bug - it's how _all_ computers store decimals, as tiny binary approximations. It almost never matters, but you should know it's there.
Heads up
For everyday display, **round when you show a number** and move on. For serious money-counting (accounting, settlement), Python offers a precise `Decimal` type for exactly this reason - we don't need it in this course, but file the name away for the day you're tallying real cash.
## Truthy and falsy
The `bool` type has a neat extra trick: _any_ value can be judged `True` or `False` when Python needs a yes/no answer. `bool()` shows you how a value will be read:
EX 3What counts as True and FalsePYch05/03_truthy.py
Copy
```
# Every value is "truthy" or "falsy" when Python treats it as a yes/no.
print("Is 0 truthy?    ", bool(0))          # False - zero is falsy
print("Is 100 truthy?  ", bool(100))        # True  - any other number
print("Empty text?     ", bool(""))         # False - an empty string is falsy
print("Some text?      ", bool("RELIANCE")) # True  - any non-empty string
```

Live output

```
Is 0 truthy?     False
Is 100 truthy?   True
Empty text?      False
Some text?       True
```

The rule is short: **zero, empty text, and "nothing" are falsy; almost everything else is truthy.** This quietly powers the decisions we'll write in Chapter 13 - `if price:` is really asking "is price something other than zero?"
## Try it yourself
  * Run `type(50 / 4)` (try it in a notebook cell, or wrap it in `print`). Is the answer an `int` or a `float`? Why?
  * Predict the output of `"7" + "7"` and then of `7 + 7`. Run both. One joins text, the other adds numbers.
  * Use `round()` to show `1405.552` to **zero** decimal places. What whole number do you get?


## Recap
  * The four everyday types are **int** (whole number), **float** (decimal), **str** (text), and **bool** (True/False); `type()` reveals any value's type.
  * Dividing whole numbers gives a **float** (`100 / 4` is `25.0`).
  * Convert with **`int()`,`float()` , `str()`** - and remember that text which _looks_ like a number (`"50"`) isn't one until you convert it.
  * **`round(value, 2)`**tidies money; decimals are stored as approximations (`0.1 + 0.2`), so round on display.
  * Values are **truthy or falsy** : zero and empty are falsy, almost everything else is truthy.


You can now store values and you know what kind each one is. Time to put them to work. In the next chapter we turn Python into a calculator - **operators** - and compute the things traders actually care about: profit, loss, and percentage moves.
On this page
