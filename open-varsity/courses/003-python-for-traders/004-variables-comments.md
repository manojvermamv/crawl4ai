Chapters
Module 1 · Getting Started with Python - Chapter 04
# Variables & Comments
Store a price, a symbol, a quantity - and leave notes for your future self. The humble building block of every program.
PY
What you'll learn
  * ·What a variable is
  * ·Storing prices & symbols
  * ·Good variable names
  * ·Reassigning values
  * ·Writing comments
  * ·Reading code aloud


Everything you'll ever build in Python rests on one humble idea: giving a name to a value so you can use it later. A price, a stock symbol, a quantity, the result of a calculation - each gets a name, and from then on you refer to it by that name. This is the **variable** , and it's the single most important concept in the whole of programming. Good news: you already understand it, because you've used it since school algebra. Let's make it concrete.
## What is a variable?
A **variable** is a named box that holds a value. You put something in the box and write a label on it; later, you fetch it by its label. In Python you create one with a single `=` sign:

```
buy_price = 1300.00

```

Read that out loud as **"buy_price gets 1300.00"** - the name on the left, the value on the right. The `=` here does _not_ mean "equals" in the maths sense; it means **"put this value into this name."** (The "are these equal?" question uses `==`, which we'll meet in Chapter 6.)
symbol "RELIANCE" quantity 50 buy_price 1300.00 A variable is a labelled box: a name on the outside, a value within.
## Storing the pieces of a trade
Variables really shine when you combine them. Here's an entire stock position described with nothing but names and arithmetic - notice how readable it is:
EX 1A whole position, in variablesPYch04/01_a_position.py
Copy
```
# A single stock position, described entirely with variables.
symbol = "RELIANCE"       # which stock we are holding
quantity = 50             # how many shares
buy_price = 1300.00       # the price we paid per share
last_price = 1313.60      # the latest market price

# Variables can be combined in calculations, just like in algebra.
invested = quantity * buy_price          # money we put in
current_value = quantity * last_price    # what the holding is worth now
profit = current_value - invested        # unrealised profit (could be negative)

print("Position:", symbol)
print("Invested:", invested)
print("Current value:", current_value)
print("Profit:", profit)
```

Live output

```
Position: RELIANCE
Invested: 65000.0
Current value: 65680.0
Profit: 680.0
```

Read it top to bottom and it almost speaks English: we hold 50 shares of RELIANCE bought at 1300, the last price is 1313.60, so the holding is worth 65,680 and we're up 680. The computer doesn't care what we _call_ things - but _we_ do, and good names turned four numbers into a story.
Key idea
A variable is just a **name pointing to a value**. You create it with `name = value`, and from then on the name stands in for the value everywhere you use it.
## Variables can change
The "variable" is well named - the value can _vary_. Point the same name at a new value any time, and the old one is simply forgotten. This is exactly how you'd track a price that keeps moving through the day:
EX 2The same name, a moving pricePYch04/02_prices_change.py
Copy
```
# A variable is not fixed - you can re-assign it a new value any time.
price = 1300.00
print("Opening price:", price)

price = 1308.75          # the market moved; point the same name at a new value
print("Midday price:", price)

price = 1313.60          # and again
print("Latest price:", price)
```

Live output

```
Opening price: 1300.0
Midday price: 1308.75
Latest price: 1313.6
```

Each `price = ...` line re-labels the box with a fresh number. There's no history kept - `price` always holds whatever you last put in it. (When we _do_ want to keep every value, we'll reach for a list, in Chapter 9.)
## Good names save you (and bad ones cost you)
Python lets you name a variable almost anything, so the discipline is on you. Compare:

```
x = 50 * 1300        # what on earth is this?
invested = quantity * buy_price   # ...oh, obviously.

```

Both run identically. One you'll understand in six months; the other you won't understand in six minutes. A few simple rules and habits:
  * Names can use **letters, digits and underscores** , but can't start with a digit and can't contain spaces.
  * The Python style is **snake_case** - lowercase words joined by underscores: `buy_price`, `last_traded_price`, `stop_loss`.
  * Spell things out. `qty` is fine, `q` is a riddle. Favour clarity over cleverness.


Tip
A good test: read your line out loud. **"current_value equals quantity times buy_price"** makes sense to a human. **"cv equals q times bp"** does not. If it reads like a sentence, you've named things well.
## Comments: notes to your future self
A **comment** is a note in your code that Python ignores completely. Anything after a `#` on a line is for human eyes only:

```
stop_loss = buy_price * 0.98   # exit if price falls 2% below our entry

```

The best comments explain the **why** , not the **what**. The code already says _what_ it does (`buy_price * 0.98`); the comment adds the bit the code can't - that this is a 2% stop. Don't narrate the obvious; explain the reasoning, the assumption, or the gotcha.
Did you know?
**Python has a hidden poem.** Type `import this` into Python and it prints "The Zen of Python" - 19 guiding principles by longtime developer Tim Peters. Among them: _"Readability counts,"_ _"Simple is better than complex,"_ and _"There should be one obvious way to do it."_ That obsession with readable code is a real reason finance teams - where one analyst must understand another's work - chose Python.
## Try it yourself
  * In `01_a_position.py`, change `quantity` to 100 and re-run. Both the value and the profit should double - one edit, ripples everywhere. That's the power of naming.
  * Rename the variable `last_price` to something shorter and worse, like `p`, everywhere it appears. It still runs - but notice how much harder the code is to read. Then change it back.
  * Add a comment above the `profit` line explaining, in your own words, _why_ it can be a negative number.


## Recap
  * A **variable** is a **name pointing to a value** , created with `name = value` ("name _gets_ value").
  * `=` means **assign** , not "equals"; combine variables in calculations just like algebra.
  * Variables can be **re-assigned** freely - the name always holds whatever you last put in it.
  * **Good names** (clear, `snake_case`, readable aloud) turn numbers into a story; bad names cost you later.
  * **Comments** (`# ...`) are notes Python ignores - use them to explain the _why_ , not the obvious _what_.


You've been writing numbers like `1300.00` and `50` without thinking about what _kind_ of thing each one is. But Python very much cares about the difference between a whole number, a decimal, a piece of text and a yes/no answer. In the next chapter we meet the basic **data types** - and learn how to convert between them.
On this page
