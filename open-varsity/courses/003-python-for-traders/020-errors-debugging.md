Chapters
Module 3 · Libraries, Files & Robust Code - Chapter 20
# Errors & Debugging
Every coder hits red text. Read a traceback calmly, catch errors with try/except, and fix the usual beginner slips.
PY
What you'll learn
  * ·Reading a traceback
  * ·Common error types
  * ·try / except
  * ·Raising your own errors
  * ·print-debugging
  * ·A calm debugging mindset


Sooner or later - usually sooner - you'll run your code and get a wall of red error text instead of an answer. Every single programmer, from day one to thirty years in, sees this constantly. The difference between a beginner and a pro isn't that the pro avoids errors; it's that the pro reads them _calmly_ , because they know an error message is not a scolding - it's a **map** to the problem. This chapter teaches you to read that map, to handle errors gracefully, and to debug without panic.
## Reading a traceback
When Python hits an error it can't continue past, it prints a **traceback** and stops. Let's cause one on purpose and look at it properly:
EX 1A deliberate crash, and the traceback it printsPYch20/01_a_traceback.py
Copy
```
# This script crashes ON PURPOSE, to show what a traceback looks like.
prices = [101.2, 103.5, 102.8]


def average(values):
    return sum(values) / len(values)


print("Average:", average(prices))   # this line works fine...
print("Bad call:", average([]))      # ...this one divides by len([]) == 0
```

Live output

```
Average: 102.5
Traceback (most recent call last):
  File "01_a_traceback.py", line 10, in <module>
    print("Bad call:", average([]))      # ...this one divides by len([]) == 0
                       ~~~~~~~^^^^
  File "01_a_traceback.py", line 6, in average
    return sum(values) / len(values)
           ~~~~~~~~~~~~^~~~~~~~~~~~~
ZeroDivisionError: division by zero
```

It looks intimidating, but it has a simple structure - and the golden rule is **read it from the bottom up** :
Traceback (most recent call last): File "trade.py", line 10, in <module> print(average([])) File "trade.py", line 6, in average return sum(v) / len(v) ZeroDivisionError: division by zero 1 read FIRST: what went wrong 2 then WHERE: file & line Read a traceback bottom-to-top - the last line names the actual error. The bottom line is the error itself; the lines above trace where it came from.
Start at the **bottom** : `ZeroDivisionError: division by zero` tells you _what_ went wrong, in plain-ish English. Then look **up** at the `File "...", line N` lines: they're a breadcrumb trail of _where_ it happened - line 10 called `average([])`, which failed at line 6 dividing by `len([])`. Python 3 even points a little `^^^` arrow at the exact spot. The error and its location: that's 90% of debugging right there.
Key idea
A **traceback** is read **bottom-up** : the last line is the **error type and message** (what went wrong), and the `File ... line N` lines above show **where** (the trail of calls that led there). Don't panic at the wall of text - jump to the bottom line first.
## Common error types
A handful of error names cover most of what you'll meet. Recognising them shortcuts the diagnosis:
  * **`SyntaxError`**- a typo in the code's structure (a missing colon or bracket). It won't even start.
  * **`NameError`**- you used a variable or function that doesn't exist (often a misspelling).
  * **`TypeError`**- an operation on the wrong type, like`"50" * "3"` or adding a number to a list.
  * **`ValueError`**- the right type but a bad value, like`int("fifty")`.
  * **`IndexError`/`KeyError`** - a list position or dictionary key that isn't there.
  * **`ZeroDivisionError`**- dividing by zero.
  * **`ModuleNotFoundError`**- a library you haven't installed (back to Chapter 19).


## try / except: surviving errors
Some errors you can _anticipate_ - an empty list, a dodgy input - and handle gracefully instead of crashing. That's what **`try`/`except`** is for: try the risky code, and if a specific error occurs, run a fallback:
EX 2Handling errors with try / exceptPYch20/02_try_except.py
Copy
```
# try/except lets your program survive an error instead of crashing.
def safe_average(values):
    try:
        return sum(values) / len(values)
    except ZeroDivisionError:
        return 0.0                       # a sensible fallback for an empty list

print("Normal:", safe_average([101.2, 103.5, 102.8]))
print("Empty :", safe_average([]))       # no crash this time

# Catching a different error - text that isn't a number.
for text in ["50", "fifty", "75"]:
    try:
        print(f"{text!r} -> {int(text)}")
    except ValueError:
        print(f"{text!r} -> not a number, skipping")
```

Live output

```
Normal: 102.5
Empty : 0.0
'50' -> 50
'fifty' -> not a number, skipping
'75' -> 75
```

The program no longer dies on an empty list or the word `"fifty"` - it returns a sensible default or skips the bad item and carries on. This is essential for code that touches the outside world (files, user input, live data), where surprises are guaranteed.
Tip
**Catch _specific_ errors**, like `except ValueError:`, not a bare `except:` that swallows _everything_. A blanket catch hides bugs you actually wanted to know about - including typos in your own code - and makes problems much harder to find. Name the error you expect.
## Raising your own errors
You can also _create_ errors deliberately, with **`raise`**, to reject bad input loudly and early rather than letting it cause a weird failure later:
EX 3Raising and catching your own errorPYch20/03_raise.py
Copy
```
# You can RAISE your own error to reject bad input early and clearly.
def position_size(capital, price):
    if price <= 0:
        raise ValueError("price must be positive")
    return int(capital // price)

print("Shares:", position_size(100000, 1313.60))

# Trigger the bad case on purpose, and catch the message we raised.
try:
    position_size(100000, 0)
except ValueError as e:
    print("Rejected:", e)
```

Live output

```
Shares: 76
Rejected: price must be positive
```

`raise ValueError("price must be positive")` stops a nonsensical call in its tracks with a clear message - far kinder than a mysterious crash three functions later. And you can `except` your own raised errors just like Python's.
Did you know?
**The first computer "bug" was a real insect.** In 1947, operators of the Harvard Mark II computer traced a malfunction to a moth stuck in a relay. They taped the moth into the logbook with the note: _"First actual case of bug being found."_ The pioneering programmer Grace Hopper helped popularise the story - and ever since, fixing code has been called _debugging_. So when your program misbehaves, you're carrying on a tradition nearly eighty years old.
## Print-debugging and a calm mindset
When the error message alone doesn't crack it, reach for the oldest, most reliable tool there is: **`print()`**. Sprinkle a few prints to see the actual values your code is working with -`print("price is", price)` - and the mismatch between what you _think_ is happening and what _is_ happening usually jumps out.
The mindset that makes it painless: read the error, find the line, look at the values, change **one thing** , run again. Errors aren't failures - they're the normal, expected feedback loop of writing code.
## Try it yourself
  * Run the crash example and read its traceback aloud, bottom to top. Then fix `average` so an empty list returns `0` instead of crashing.
  * Trigger a `KeyError` on purpose: make a dict `q = {"ltp": 100}` and ask for `q["bid"]`. Read the error, then rewrite it safely with `.get()`.
  * Wrap `int(input("Quantity: "))` in a `try/except ValueError` that prints "please enter a whole number" when the user types text.


## Recap
  * A **traceback** is a map: read it **bottom-up** - error type and message first, then the **file and line** where it happened.
  * Know the common errors - **`NameError`,`TypeError` , `ValueError`, `KeyError`, `IndexError`, `ModuleNotFoundError`** - to diagnose faster.
  * **`try`/`except`** handles anticipated errors gracefully; catch **specific** exceptions, never a bare `except:`.
  * **`raise`**lets you reject bad input early with a clear message.
  * **Print-debugging** and changing **one thing at a time** beat panic every time.


You can now write robust code that survives surprises. Next we give your programs a memory beyond a single run - the ability to **read and write files** , so you can load data from disk and save your results to keep.
On this page
