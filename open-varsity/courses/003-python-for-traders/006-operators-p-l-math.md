Chapters
Module 1 · Getting Started with Python - Chapter 06
# Operators & P&L Math
Add, subtract, compare and combine - using Python as a calculator to work out profit, loss and percentage moves.
PY
What you'll learn
  * ·Arithmetic operators
  * ·Computing profit & loss
  * ·Percentage change
  * ·Comparison operators
  * ·Logical and / or / not
  * ·Operator precedence


A trader's day is full of small sums: what's my profit, what's the percentage move, how many lots can I afford, is the price above my level? Python does every one of these instantly, and the symbols it uses - **operators** - are mostly the ones you already know from a calculator. In this chapter we'll meet the full set and put them straight to work on profit, loss and percentage change. By the end you'll be doing real trade maths in code.
## The arithmetic operators
Four symbols cover almost everything: `+` add, `-` subtract, `*` multiply, `/` divide. Here they are computing a complete trade result:
EX 1Profit, loss and percentage changePYch06/01_pnl.py
Copy
```
# The four everyday arithmetic operators, on a real trade.
buy_price = 1300.00
sell_price = 1313.60
quantity = 50

profit_per_share = sell_price - buy_price                 # subtraction
total_profit = profit_per_share * quantity                # multiplication
pct_change = (sell_price - buy_price) / buy_price * 100    # division, then x100

print("Profit per share:", round(profit_per_share, 2))
print("Total profit    :", round(total_profit, 2))
print("Percentage change:", round(pct_change, 2), "%")
```

Live output

```
Profit per share: 13.6
Total profit    : 680.0
Percentage change: 1.05 %
```

The first two lines are plain shopkeeper maths. The third is the one every trader lives by - **percentage change** - so let's slow down and name its parts:
percentage change ( new - old ) / old × 100 ( 1313.60 - 1300.00 ) / 1300.00 × 100 = +1.05 % Percentage change: how far the new price moved, measured against the old one.
You take the change (`new - old`), divide by where you started (`old`), and multiply by 100 to make it a percentage. RELIANCE moving from 1300 to 1313.60 is a `+1.05%` day. This one formula reappears constantly - daily returns, gains, drawdowns - so it's worth knowing in your bones.
## Three more: floor division, remainder and power
Three less obvious operators each earn their keep in trading:
EX 2Floor division, remainder, power - and precedencePYch06/02_more_operators.py
Copy
```
# Three more operators worth knowing, each with a trading use.
capital = 100000
cost_per_lot = 65680

print("Whole lots affordable:", capital // cost_per_lot)   # // floor division
print("Cash left over       :", capital % cost_per_lot)    # %  remainder
print("1% a day for 5 days  :", round((1.01 ** 5 - 1) * 100, 2), "%")  # ** power

# Operator precedence: * and / happen before + and - (just like school maths).
print("1000 + 50 * 2   =", 1000 + 50 * 2)        # 1100, not 2100
print("(1000 + 50) * 2 =", (1000 + 50) * 2)      # 2100 - parentheses win
```

Live output

```
Whole lots affordable: 1
Cash left over       : 34320
1% a day for 5 days  : 5.1 %
1000 + 50 * 2   = 1100
(1000 + 50) * 2 = 2100
```

  * **`//`floor division** throws away the remainder - perfect for "how many _whole_ lots can I afford with this capital?" (the answer is `1`, not `1.52`).
  * **`%`modulo** gives you the remainder - the leftover cash after buying those whole lots.
  * **`**`power** raises to an exponent - ideal for compounding, like growing 1% a day for 5 days.


The last two lines show **operator precedence** : Python follows the same order as school maths - `*` and `/` happen before `+` and `-`. So `1000 + 50 * 2` is `1100`, not `2100`.
Tip
When in doubt, **use parentheses**. `(1000 + 50) * 2` leaves no room for confusion, and even when they're not strictly needed, they make your intent obvious to the next human who reads the line - which is often future you.
## Asking questions: comparison operators
The operators so far produce numbers. **Comparison operators** produce a `True` or `False` - they ask a yes/no question:
EX 3Comparisons and logic return True or FalsePYch06/03_comparisons_logic.py
Copy
```
# Comparison operators ask a yes/no question and return True or False.
price = 1313.60
support = 1300.00
resistance = 1325.00

print("Above support?   ", price > support)       # True
print("Below resistance?", price < resistance)     # True
print("Exactly 1300?    ", price == 1300.00)       # False  (== means "equal to")

# Logical operators combine yes/no answers.
in_range = price > support and price < resistance  # both must be True
print("Inside the range?", in_range)               # True
print("Outside the range?", not in_range)          # the opposite
```

Live output

```
Above support?    True
Below resistance? True
Exactly 1300?     False
Inside the range? True
Outside the range? False
```

The full set is `>` greater than, `<` less than, `>=` at least, `<=` at most, `==` equal to, and `!=` not equal. Note the double `==` for "is it equal?" - a single `=` _assigns_ a value (Chapter 4), while `==` _compares_. Mixing them up is a rite of passage; now you've been warned.
## Combining questions: and, or, not
Real trading rules stack several conditions: "price above support **and** below resistance," "near the open **or** near the close." Three **logical operators** glue yes/no answers together:
  * **`and`**- True only when _both_ sides are True.
  * **`or`**- True when _at least one_ side is True.
  * **`not`**- flips True to False and back.


The surest way to learn them is a **truth table** - every combination of two yes/no inputs, with what each operator gives back:
ABA and BA or Bnot A TrueTrueTrueTrueFalse TrueFalseFalseTrueFalse FalseTrueFalseTrueTrue FalseFalseFalseFalseTrue and needs both True; or needs just one; not simply flips it. (green = True, red = False)
Read the rows like sentences: `True and False` is `False` (both must hold), but `True or False` is `True` (one is enough). In the example, `price > support and price < resistance` is True only because the price clears _both_ tests. These little expressions are the seed of every trading rule you'll ever write - and in Chapter 13 we'll wire them into `if` statements that actually _act_ on the answer.
Key idea
**Arithmetic** (`+ - * / // % **`) makes numbers; **comparisons** (`> < >= <= == !=`) make True/False; **logic** (`and or not`) combines True/False. That's the whole toolkit for turning prices into decisions.
Did you know?
**One tiny operator once shook the whole Python world.** In 2018 the language added the "walrus operator" `:=` (it looks like a walrus's eyes and tusks). The debate over it grew so heated that Python's creator, Guido van Rossum, stepped down as the project's "Benevolent Dictator For Life" - the title he'd held since 1991 - handing decisions to a steering council instead. Proof that in programming, even a two-character symbol can be a very big deal.
## Try it yourself
  * Change `sell_price` in the first example to `1287.00` (a loss). What sign do the profit and percentage now carry?
  * Using `**`, work out the value of 100,000 growing at 12% a year for 10 years: `100000 * 1.12 ** 10`. (Compounding is just the power operator.)
  * Write a single line that is `True` only if a `price` of 1313.60 is **both** above 1300 **and** not equal to 1320.


## Recap
  * The arithmetic operators are `+ - * /`, plus **`//`**(whole-number division),**`%`**(remainder) and**`**`**(power).
  * **Percentage change** = `(new - old) / old * 100` - the trader's most-used formula.
  * **Precedence** follows school maths (`*`,`/` before `+`,`-`); reach for **parentheses** to be clear.
  * **Comparison** operators (`> < >= <= == !=`) return `True`/`False`; remember `==` compares, `=` assigns.
  * **Logical** operators **`and`/`or` / `not`** combine yes/no answers - the building blocks of trading rules.


You can now calculate and compare. But so far every number has been hard-coded into the script. In the next chapter we make programs that _talk_ : printing results cleanly and reading values in - and we'll meet **f-strings** , the elegant way to format rupees, dollars and percentages so they look exactly right.
On this page
