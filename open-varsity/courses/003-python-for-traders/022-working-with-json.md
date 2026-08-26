Chapters
Module 3 · Libraries, Files & Robust Code - Chapter 22
# Working with JSON
JSON is how market APIs talk. Turn a JSON string into a Python dict and back - the format you'll meet again and again.
PYNSE
What you'll learn
  * ·What JSON is
  * ·json.loads & dumps
  * ·JSON <-> dict
  * ·Nested market data
  * ·Reading a JSON file
  * ·Pretty-printing


We've bumped into JSON twice now - in the standard-library tour, and as the shape of a nested dictionary. It's time to meet it properly, because **JSON is the language market data speaks.** Ask almost any trading or data API for a quote, a candle, or an order book, and it answers in JSON. Once you can turn that text into Python and back, a whole world of live data opens up - and the best part is you already understand 90% of it, because JSON is basically a dictionary in disguise.
## What is JSON?
**JSON** - JavaScript Object Notation - is just a text format for structured data. It looks almost exactly like the Python dictionaries and lists you already know. The `json` module translates between JSON _text_ and Python _objects_ with two workhorse functions:
EX 1json.loads and json.dumps, with pretty-printingPYch22/01_loads_dumps.py
Copy
```
import json

# A JSON string - exactly the kind of text a market API sends back.
text = '{"symbol": "RELIANCE", "ltp": 1313.60, "exchange": "NSE"}'

quote = json.loads(text)              # JSON text -> Python dict
print("Price:", quote["ltp"])
print("Type :", type(quote).__name__)

# The other direction, with indent= for a human-readable layout.
nice = json.dumps(quote, indent=2)
print(nice)
```

Live output

```
Price: 1313.6
Type : dict
{
  "symbol": "RELIANCE",
  "ltp": 1313.6,
  "exchange": "NSE"
}
```

`json.loads` takes JSON text and gives you a Python dict (note it really is a `dict` - so all your `["key"]` skills apply). `json.dumps` goes the other way, and `indent=2` lays it out readably. Picture the two sides:
JSON text Python dict { "symbol": "RELIANCE", "ltp": 1313.6, "active": true } { 'symbol': 'RELIANCE', 'ltp': 1313.6, 'active': True } json.loads json.dumps loads turns JSON text into a Python dict; dumps turns it back. Note how true becomes True.
Key idea
**`json.loads(text)`**parses JSON text into a Python dict/list.**`json.dumps(obj)`**turns a Python object back into JSON text (`indent=` makes it readable). JSON's structure mirrors Python's dictionaries and lists almost exactly.
## Nested market data
Real responses are rarely flat - a quote wraps a status, which wraps data, which wraps an order book. You navigate the layers by chaining keys and list indexes:
EX 2Digging through a nested API responsePYch22/02_nested.py
Copy
```
# Real API responses are nested: dictionaries inside dictionaries inside lists.
response = {
    "status": "success",
    "data": {
        "symbol": "RELIANCE",
        "ltp": 1313.60,
        "depth": {
            "buy":  [{"price": 1313.55, "qty": 120}, {"price": 1313.50, "qty": 80}],
            "sell": [{"price": 1313.65, "qty": 95},  {"price": 1313.70, "qty": 150}],
        },
    },
}

# Dig through the layers with keys and list indexes.
data = response["data"]
print("Symbol   :", data["symbol"])
print("LTP      :", data["ltp"])
print("Best buy :", data["depth"]["buy"][0]["price"])    # first buy order's price
print("Best sell:", data["depth"]["sell"][0]["price"])
```

Live output

```
Symbol   : RELIANCE
LTP      : 1313.6
Best buy : 1313.55
Best sell: 1313.65
```

`response["data"]["depth"]["buy"][0]["price"]` reads left to right like directions: into `data`, into `depth`, into the `buy` list, take the _first_ order `[0]`, read its `price`. It looks daunting written out, but you build it one step at a time - and it's exactly the shape a live market-depth feed has (you'll see the real thing in Chapter 37).
Tip
When a nested response confuses you, **pull it apart in stages**. Assign `data = response["data"]`, print it, then go one level deeper: `depth = data["depth"]`. Inspecting each layer as you descend beats guessing at one long chain of brackets - and it's far easier to debug.
## Reading and writing JSON files
To save structured data to disk, or load a JSON file someone gave you, use **`json.dump`**and**`json.load`**- the _file_ versions (note: no "s" on the end):
EX 3Saving and loading a JSON filePYch22/03_json_file.py
Copy
```
import json

watchlist = {"RELIANCE": 1313.60, "TCS": 2109.00, "INFY": 1056.60}

# json.dump (no "s") writes a dict straight to a FILE.
with open("watchlist.json", "w") as f:
    json.dump(watchlist, f, indent=2)

# json.load (no "s") reads a FILE straight back into a dict.
with open("watchlist.json") as f:
    loaded = json.load(f)

print("Loaded:", loaded)
print("TCS   :", loaded["TCS"])
```

Live output

```
Loaded: {'RELIANCE': 1313.6, 'TCS': 2109.0, 'INFY': 1056.6}
TCS   : 2109.0
```

This is the one naming trap in the whole module: `dumpS`/`loadS` (with an `s`) work with **strings** ; `dump`/`load` (no `s`) work with **files**. Remember "s for string" and you'll never mix them up.
Did you know?
**JSON came from JavaScript - but Python speaks it fluently.** JSON was distilled from JavaScript around 2001 and has since become the lingua franca of the web; almost every API on earth, trading APIs included, answers in it. The lucky break for us is that JSON's curly-brace, key-value shape is nearly identical to a Python dictionary. The tiny differences - JSON writes `true`/`false`/`null` where Python writes `True`/`False`/`None` - are translated for you automatically by the `json` module, so you hardly notice.
## The small gotchas
JSON and Python dicts look alike but aren't _identical_ , and the differences trip up beginners exactly once:
  * JSON uses **`true`/`false` / `null`** (lowercase); Python uses **`True`/`False` / `None`**. The `json` module converts both ways for you.
  * JSON keys and text **must use double quotes** (`"symbol"`), never single. Python is relaxed about quotes; JSON is strict.
  * JSON is always **text** until you `loads` it - so `quote["ltp"]` only works _after_ parsing, not on the raw string.


Know these three and you'll read any API response with confidence.
## Try it yourself
  * Take the JSON string `'{"qty": 50, "filled": false}'`, parse it with `json.loads`, and check what Python value `filled` becomes.
  * From the nested `response`, print the _second_ sell order's quantity. (Mind the `[1]` index.)
  * Build a small dict of three symbols and prices, `json.dumps` it with `indent=2`, and print the result - the shape an API would send.


## Recap
  * **JSON** is the text format nearly every market API uses; it mirrors Python dicts and lists.
  * **`json.loads`**parses JSON text to a Python object;**`json.dumps`**serialises back (use`indent=` to pretty-print).
  * For files, **`json.load`**/**`json.dump`**(no "s"); for strings,**`loads`**/**`dumps`**("s for string").
  * Navigate **nested** data by chaining keys and indexes, one layer at a time.
  * Mind the gotchas: **`true`/`false` /`null`** vs **`True`/`False` /`None`**, and JSON's mandatory **double quotes**.


JSON handles the _structure_ of market data, but one field in it always needs special care: the **timestamp**. Dates and times have their own quirks - time zones, formats, market sessions - so the next chapter gives them the attention they deserve.
On this page
