Chapters
Module 3 · Libraries, Files & Robust Code - Chapter 17
# Modules & Imports
Python comes with batteries included. Learn to import ready-made tools - and split your own code into tidy files.
PY
What you'll learn
  * ·What a module is
  * ·import & from-import
  * ·Aliasing with as
  * ·The math & statistics modules
  * ·Your own module
  * ·Where Python looks


Welcome to **Module 3** , where your toolkit gets a serious upgrade. So far you've written everything from scratch. But one of Python's superpowers - the reason we called it a "glue language" back in Chapter 1 - is that you rarely have to. Need a square root, a calendar, randomness, a way to read a file? Someone has already written it, tested it, and shipped it. You just have to **import** it. This chapter is about how to reach those ready-made tools, and how to organise your own code the same way.
## What is a module?
A **module** is simply a file of Python code - functions and values - that you can pull into your program. Python ships with hundreds of them, collectively called the **standard library** , covering maths, dates, files, randomness and far more. You bring one in with **`import`**and then reach inside it with a dot:
EX 1Importing the math and statistics modulesPYch17/01_math_statistics.py
Copy
```
# "import" brings a ready-made module into your program.
import math
import statistics

closes = [101.2, 103.5, 102.8, 104.1, 105.6]

print("Square root of 2:", round(math.sqrt(2), 4))   # reach a function with module.name
print("Pi              :", round(math.pi, 4))         # ...and constants too
print("Average close   :", statistics.mean(closes))
print("Std deviation   :", round(statistics.stdev(closes), 4))
```

Live output

```
Square root of 2: 1.4142
Pi              : 3.1416
Average close   : 103.44
Std deviation   : 1.6227
```

Python Standard Library - "batteries included" math statistics datetime json random os import import math math.sqrt(2) -> 1.4142 import lifts a ready-made tool off the standard-library shelf and into your program.
`import math` makes the whole `math` module available, and you use its pieces as `math.sqrt`, `math.pi`, and so on. The dot says "look _inside_ math for this." No installing, no setup - these come with Python.
Key idea
A **module** is a file of reusable code. **`import math`**loads it, and you reach its contents with a dot:**`math.sqrt(2)`**. Python's built-in**standard library** has hundreds of such modules, free and ready.
## Three ways to import
There's more than one way to bring code in, and each reads a little differently:
EX 2import, from-import, and import-asPYch17/02_import_styles.py
Copy
```
# Three ways to bring code in, each handy in different situations.
import math                            # whole module:   math.sqrt(...)
from statistics import mean, stdev     # specific names:  mean(...)
import statistics as st                # an alias:        st.variance(...)

closes = [101.2, 103.5, 102.8, 104.1, 105.6]

print("Hypotenuse:", math.hypot(3, 4))             # module.name
print("Mean      :", mean(closes))                 # imported name, used directly
print("Variance  :", round(st.variance(closes), 4))  # alias.name
```

Live output

```
Hypotenuse: 5.0
Mean      : 103.44
Variance  : 2.633
```

  * **`import math`**- load the module; use`math.hypot(...)`. Clear about where things come from.
  * **`from statistics import mean, stdev`**- pull specific names in so you can use them bare:`mean(...)`.
  * **`import statistics as st`**- load it under a short**alias** , then `st.variance(...)`. You'll see this constantly in Module 4 as `import pandas as pd`.


Tip
Avoid `from module import *` (import _everything_). It dumps every name from the module into your code, where it can silently clash with your own variables and leaves a reader guessing where things came from. Be explicit - import the module, or the specific names you need.
## Your own module
Here's the lovely part: a module is _just a .py file_. The moment you save functions in their own file, you've made a module you can import - exactly like a built-in one. Here's a little `tradetools.py`:
EX 3tradetools.py - a module of your ownPYch17/tradetools.py
Copy
```
# A module is simply a .py file of functions you can import elsewhere.
# Save this as tradetools.py, then import it from another script.
def pnl(buy, sell, qty):
    """Profit on a completed round-trip trade."""
    return (sell - buy) * qty


def pct_change(old, new):
    """Percentage change from old price to new."""
    return (new - old) / old * 100
```

And another script that imports and uses it:
EX 4Importing your own modulePYch17/03_use_module.py
Copy
```
# Import your own module exactly like a built-in one (no ".py" in the name).
import tradetools

print("P&L      :", round(tradetools.pnl(1300, 1313.60, 50), 2))
print("Change % :", round(tradetools.pct_change(1300, 1313.60), 2))
```

Live output

```
P&L      : 680.0
Change % : 1.05
```

`import tradetools` finds `tradetools.py` and gives you its functions as `tradetools.pnl(...)`. Note: no `.py` in the import. **Where does Python look?** First in the same folder as your script, then through the libraries you've installed - which is the subject of the next chapter. This is how you keep a growing project tidy: related functions live together in their own files.
Did you know?
**Python has a flying easter egg.** Open Python and type `import antigravity` - it pops open your web browser to a famous xkcd comic in which a character discovers he can fly, simply by importing Python. It's a wink built right into the language by its own developers, and a nod to the "batteries included" joke: Python has a module for _everything_ , apparently even gravity.
## Try it yourself
  * Import `math` and print `math.floor(76.12)` and `math.ceil(76.12)` - the "how many whole lots" idea from Chapter 6, done two ways.
  * Use `from statistics import median` to print the median of `[101.2, 103.5, 102.8, 104.1, 105.6]`.
  * Add a third function to `tradetools.py` - say `target_price(buy, pct)` - then import and call it from another script.


## Recap
  * A **module** is a file of reusable code; **`import`**loads it and you access its contents with a**dot** (`math.sqrt`).
  * Python's **standard library** ships hundreds of modules - "batteries included", no install required.
  * Import styles: **`import module`**,**`from module import name`**, and**`import module as alias`**- avoid`import *`.
  * **Your own`.py` files are modules too** - import them to keep projects organised. Python looks in your folder first, then installed libraries.


The standard library is so useful it deserves a proper tour. In the next chapter we'll open the most valuable drawers for a trader - dates and times, random numbers for simulation, and the JSON tools that read market data - so you know what's already at your fingertips.
On this page
