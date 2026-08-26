Chapters
Module 2 · Core Programming - Chapter 11
# Dictionaries
Look things up by name, not position. A live quote - symbol, price, volume - is a dictionary, the most useful structure in finance code.
PYNSE
What you'll learn
  * ·Key-value pairs
  * ·A quote as a dict
  * ·Getting & setting values
  * ·Looping over a dict
  * ·Nested dictionaries
  * ·get() & defaults


Lists and tuples find things by _position_ : "give me the third item." But in trading you far more often want to find things by _name_ : "what's the last price of RELIANCE?" You don't care whether it's the third or the thirtieth stock - you know its name. The structure built for exactly this is the **dictionary** , and it is, without exaggeration, the most useful container in all of finance code. A live quote is a dictionary. An API response is a dictionary. A row of data is a dictionary. Master this one and a huge amount of real-world code suddenly makes sense.
## Looking up by name, not position
A dictionary is a set of **key-value pairs** , written with curly braces. Each _key_ (a name) points to a _value_. You look things up, update them, and add new ones - all by key:
EX 1A live quote modelled as a dictionaryPYch11/01_a_quote.py
Copy
```
# A dictionary stores values you look up by NAME (a "key"), not by position.
quote = {
    "symbol": "RELIANCE",
    "ltp": 1313.60,
    "change": 13.60,
    "volume": 4521000,
}

print("Symbol:", quote["symbol"])     # look up a value by its key
print("Price :", quote["ltp"])

quote["ltp"] = 1315.20                 # update an existing value
quote["high"] = 1318.40                # add a brand-new key
print("Updated:", quote)
```

Live output

```
Symbol: RELIANCE
Price : 1313.6
Updated: {'symbol': 'RELIANCE', 'ltp': 1315.2, 'change': 13.6, 'volume': 4521000, 'high': 1318.4}
```

quote (a dictionary): key → value "symbol" "ltp" "change" "volume" "RELIANCE" 1313.60 13.60 4521000 A dictionary maps each key (a name) to a value. quote["ltp"] follows the arrow to 1313.60.
`quote["ltp"]` reads "follow the `ltp` arrow" and lands on `1313.60`. Assigning to a key either **updates** it (if it exists) or **creates** it (if it doesn't) - that's how `quote["high"] = 1318.40` added a new field on the spot.
Key idea
A **dictionary** `{"key": value, ...}` stores **key-value pairs**. Look up, update, or add with `dict[key]`. Keys are usually strings (names); values can be anything - numbers, text, even other dictionaries.
## Looping over a dictionary, safely
To walk through a dictionary, `.items()` gives you each key and value together. And to fetch a key that _might not exist_ , `get()` saves you from a crash:
EX 2Looping with .items() and the safe .get()PYch11/02_loop_and_get.py
Copy
```
quote = {"symbol": "RELIANCE", "ltp": 1313.60, "change": 13.60}

# .items() hands you each key and its value together - perfect for a loop.
for field, value in quote.items():
    print(f"{field:>8}: {value}")

# get() safely fetches a key, returning a fallback if it's missing - no crash.
print("Bid       :", quote.get("bid", "not available"))
```

Live output

```
  symbol: RELIANCE
     ltp: 1313.6
  change: 13.6
Bid       : not available
```

Tip
Asking for a missing key with square brackets - `quote["bid"]` when there's no bid - raises a `KeyError` and stops your program. **`quote.get("bid", "not available")`**instead returns your fallback and carries on. When you're unsure a key is present (very common with live data), reach for`get()`.
## Dictionaries inside dictionaries
Values can themselves be dictionaries, and this is where it gets powerful. A whole watchlist becomes a dictionary of quotes, keyed by symbol:
EX 3A nested dictionary - a watchlist of quotesPYch11/03_nested.py
Copy
```
# Dictionaries can hold dictionaries - here, a watchlist keyed by symbol.
watchlist = {
    "RELIANCE": {"ltp": 1313.60, "change": 13.60},
    "TCS":      {"ltp": 2109.00, "change": -8.50},
    "INFY":     {"ltp": 1056.60, "change": 4.20},
}

print("TCS price:", watchlist["TCS"]["ltp"])    # dig in with two keys
print("Symbols  :", list(watchlist.keys()))     # all the keys as a list

# Loop through every quote in the watchlist.
for symbol, data in watchlist.items():
    print(f"{symbol:9} ltp {data['ltp']:>9.2f}  change {data['change']:+.2f}")
```

Live output

```
TCS price: 2109.0
Symbols  : ['RELIANCE', 'TCS', 'INFY']
RELIANCE  ltp   1313.60  change +13.60
TCS       ltp   2109.00  change -8.50
INFY      ltp   1056.60  change +4.20
```

You dig in with two keys: `watchlist["TCS"]["ltp"]` means "the TCS entry, then its ltp." If this shape looks important, that's because it is - it's almost exactly the **JSON** format that market APIs send back. We'll meet JSON properly in Chapter 22, and you'll find you already understand it.
Did you know?
**Dictionary look-ups are almost instant - and stay that way no matter how big the dictionary grows.** Whether it holds ten quotes or ten million, fetching one by its key takes about the same tiny moment, thanks to a clever structure called a _hash table_. (Bonus: since Python 3.7, dictionaries also remember the exact order you added keys in.) It's why dictionaries quietly power so much fast software - including parts of Python itself.
## Why dictionaries matter so much
It's worth pausing on just how often this one structure shows up:
  * A **live quote** - symbol, price, volume, bid, ask - is a dictionary.
  * A **JSON response** from any trading or data API is dictionaries (often nested).
  * A **row** in a pandas DataFrame behaves like a dictionary, keyed by column name.
  * Configuration, settings, lookups by name - all dictionaries.


Get comfortable here and you've got a key (pun intended) that unlocks Modules 3 and 4.
## Try it yourself
  * Build a dictionary for a TCS quote with keys `symbol`, `ltp` and `change`, then print just the price.
  * Use `.get()` to ask your quote for a `"sector"` key it doesn't have, with the fallback `"unknown"`.
  * From the nested `watchlist`, print every symbol whose `change` is positive. (Hint: loop with `.items()` and check `data["change"]` - we'll formalise the "check" in the next chapters.)


## Recap
  * A **dictionary** `{key: value}` looks values up by **name** , not position - perfect for quotes, records and settings.
  * Read/update/add with `dict[key]`; assigning to a new key **creates** it.
  * Loop with **`.items()`**(key and value together); fetch safely with**`.get(key, default)`**to avoid a`KeyError`.
  * **Nested dictionaries** model a watchlist of quotes - and mirror the **JSON** that APIs return.
  * Dictionaries are **fast** (hash tables) and, since Python 3.7, keep their **insertion order**.


You've now met the four core collections: lists, tuples, dictionaries - and one more to go. When all you care about is membership and uniqueness - "which symbols are in _both_ my watchlists?" - there's a specialised tool that's perfect, and fast. Next up: the **set**.
On this page
