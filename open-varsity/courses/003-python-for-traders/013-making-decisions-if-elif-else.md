Chapters
Module 2 · Core Programming - Chapter 13
# Making Decisions: if / elif / else
Teach your code to choose - buy, sell or hold - with conditions and the boolean logic underneath them.
PY
What you'll learn
  * ·if / elif / else
  * ·Boolean conditions
  * ·Combining with and / or
  * ·A simple buy / sell rule
  * ·Nested conditions
  * ·Guard clauses


Up to now your programs have run straight through, top to bottom, doing the same thing every time. Real tools aren't like that - they _decide_. "If the price is above its average, flag a buy. Otherwise, hold." That word "if" is where programming starts to feel powerful, and Python spells it exactly that way. In this chapter your code learns to choose, and you'll write your first genuine trading rule.
## The if statement
An `if` runs a block of code **only when a condition is True**. You write the condition (one of those True/False expressions from Chapter 6), end the line with a colon, and **indent** the code that should run:
EX 1Classifying a day with if / elif / elsePYch13/01_if_elif_else.py
Copy
```
# if / elif / else runs the FIRST branch whose condition is True, then stops.
change_pct = 1.05      # today's percentage change

if change_pct >= 2:
    print("Big move up (2% or more)")
elif change_pct > 0:
    print("Small gain")
elif change_pct == 0:
    print("Flat - no change")
else:
    print("Down day")
```

Live output

```
Small gain
```

Read it as a cascade. Python checks each condition from the top and runs the **first** block whose condition is `True` - then skips all the rest. Our `change_pct` of `1.05` isn't `>= 2`, but it _is_ `> 0`, so "Small gain" prints and the `==0` and `else` branches are never even looked at.
change_pct change > 0 ? True print("Gain") False change < 0 ? True print("Loss") False print("Flat") Each condition is tested in turn; the first True branch runs, and the rest are skipped.
`if` starts the chain, `elif` ("else if") adds more conditions, and `else` is the catch-all that runs when nothing above matched. You can have as many `elif`s as you like - or none at all.
Key idea
**`if`condition`:`** runs its indented block when the condition is `True`. **`elif`**adds another test,**`else`**catches everything left over. Only the**first** matching branch runs.
## Indentation is the syntax
Look again at where the `print` lines sit: pushed in from the left. That indentation isn't decoration - in Python, **it's how the language knows which lines belong to the`if`.** The indented lines are "inside"; when the indentation stops, the block is over. The standard is **four spaces** per level (any decent editor inserts them when you press Tab).
Did you know?
**In most languages, indentation is just good manners. In Python, it's the law.** Where languages like C, Java and JavaScript mark blocks with curly braces `{ }` and treat spacing as optional decoration, Python uses the indentation _itself_ to define blocks - a design called the "off-side rule." Guido van Rossum chose it deliberately to force code to be readable, ending decades of arguments about where the braces should go. It's one of the first things people notice about Python, and one they quickly come to love.
## Building a trading rule
Conditions get interesting when you combine them with the `and` / `or` from Chapter 6. Here's a real, if simple, signal:
EX 2A buy / sell / hold rule from two conditionsPYch13/02_buy_sell_rule.py
Copy
```
# A plain-English trading rule, written as conditions with and / or.
price = 1313.60
sma = 1305.00      # the 20-day simple moving average
rsi = 45           # a momentum gauge: above 70 = overbought, below 30 = oversold

if price > sma and rsi < 70:
    signal = "BUY"      # above the average, and not overbought
elif price < sma and rsi > 30:
    signal = "SELL"     # below the average, and not oversold
else:
    signal = "HOLD"

print("Price above average?", price > sma)
print("Signal:", signal)
```

Live output

```
Price above average? True
Signal: BUY
```

The rule reads almost like English: buy when the price is above its moving average **and** momentum isn't overbought. With `price` above `sma` and `rsi` a calm `45`, both parts of the BUY condition hold, so `signal` becomes `"BUY"`. This is the seed of every systematic strategy - a set of conditions that map market data to a decision.
## Guard clauses: handle the bad cases first
When you have several things that could go wrong, the cleanest style is to **check the bad cases first and bail out** , leaving the "everything's fine" path for last:
EX 3Validating an order with guard clausesPYch13/03_guard_clause.py
Copy
```
# Guard clauses: check the bad cases first and reject early, so the
# "happy path" at the end runs only when everything is in order.
capital = 100000
price = 1313.60
quantity = 50

cost = price * quantity

if quantity <= 0:
    print("Reject: quantity must be positive.")
elif cost > capital:
    print(f"Reject: need {cost:,.0f} but only have {capital:,.0f}.")
else:
    print(f"Order OK: {quantity} shares for {cost:,.2f}. Cash left {capital - cost:,.2f}.")
```

Live output

```
Order OK: 50 shares for 65,680.00. Cash left 34,320.00.
```

We reject a non-positive quantity, then reject an order we can't afford, and only if both checks pass do we confirm it. This "guard clause" style keeps logic flat and readable - far nicer than burying the real work inside layers of nested `if`s.
Tip
You _can_ nest an `if` inside another `if` (inside another...), but deep nesting quickly becomes hard to follow. Prefer **guard clauses** - a few early checks that handle the exceptions up front - so your main logic stays at the left margin where it's easy to read.
## Try it yourself
  * Change `change_pct` to `2.5`, then `-0.4`, then `0`, and predict which branch prints before you run it.
  * In the buy/sell rule, set `rsi = 75` (overbought). Does the BUY condition still hold? What signal do you get now?
  * Add a third guard clause to the order check that rejects the trade if `price <= 0`.


## Recap
  * **`if condition:`**runs an indented block when the condition is True;**`elif`**adds more tests,**`else`**catches the rest - only the**first** match runs.
  * **Indentation defines blocks** in Python (four spaces); it's part of the syntax, not just style.
  * Combine conditions with **`and`/`or`** to express real trading rules in near-English.
  * Prefer **guard clauses** (check bad cases early) over deeply **nested** conditions for readable code.


Your code can now make a single decision. But a watchlist has dozens of stocks, and a price history has thousands of days - you'll want to apply a decision to _every one of them_ without writing it out by hand. That repetition engine is the **loop** , and it's next.
On this page
